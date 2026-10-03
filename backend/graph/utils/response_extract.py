"""
Ground-Truth Highlight Extraction
==================================

The LLM writes good prose but is not reliable at transcribing exact
field values into structured output — it can produce a correct
sentence ("...patient Harsh Kumar...") while, in the same call,
writing "-" for a structured `Name` highlight. That's a real bug
class in clinical UI: the doctor is looking at the highlight chips,
not re-reading the prose, so a wrong or blank chip is what they act
on.

This module pulls a small set of safety-critical identity facts —
patient id/name/gender/DOB, drug name/dosage/frequency, status —
straight out of the raw backend result with plain Python, and
`response_agent` uses it to correct or fill in whatever the LLM
produced. These values never pass through the LLM, so they can't be
misremembered or replaced with a placeholder.
"""

import re

# (display label, keys to look for, optional value transformer)
_FIELD_SPECS = [
    ("Patient ID", ("id", "patient_id"), None),
    ("Name", ("name", "patient_name", "full_name"), "name"),
    ("Gender", ("gender",), None),
    ("Birth Date", ("birth_date", "birthdate", "birthdate_", "dob"), None),
    ("Medicine", ("medicine_name", "medication_name", "drug_name"), None),
    ("Dosage", ("dosage",), None),
    ("Frequency", ("frequency",), None),
    ("Status", ("status",), None),
]

# Fixed, sensible display order regardless of what order fields were
# found in — keeps the card layout predictable.
_DISPLAY_ORDER = [label for label, _, _ in _FIELD_SPECS]


def _extract_name(value):
    """
    Accepts a plain flattened string ("Harsh Kumar"), or a raw FHIR
    HumanName list/dict ([{"given": ["Harsh"], "family": "Kumar"}]),
    and returns a clean display string either way.
    """

    if isinstance(value, str):
        return value.strip() or None

    if isinstance(value, dict):
        value = [value]

    if isinstance(value, list) and value:
        entry = value[0] or {}

        if isinstance(entry, str):
            return entry.strip() or None

        given = entry.get("given", [])
        family = entry.get("family", "")

        given_text = (
            " ".join(str(v) for v in given if v)
            if isinstance(given, list)
            else str(given or "")
        )

        full = f"{given_text} {family or ''}".strip()

        return full or None

    return None


_TRANSFORMS = {
    "name": _extract_name,
}


def _find(d: dict, keys: tuple[str, ...]):
    """Case-insensitive lookup of the first matching key in a dict."""

    lowered = {k.lower(): k for k in d}

    for key in keys:
        actual = lowered.get(key)

        if actual is not None:
            return d[actual]

    return None


def ground_truth_highlights(result, max_items: int = 6):
    """
    Returns a list of (label, value) tuples for whichever of the
    known identity fields are actually present in `result` — shallow,
    plus one level into a nested "patient" / "resolved_patient"
    object, since that's the common shape across agents and
    workflows. Never guesses, never invents: a field that isn't
    there is simply absent from the result, not filled with a
    placeholder.
    """

    if not isinstance(result, dict):
        return []

    candidates = [result]

    for nested_key in ("patient", "resolved_patient"):
        nested = result.get(nested_key)

        if isinstance(nested, dict):
            candidates.append(nested)

    found: dict[str, str] = {}

    for d in candidates:
        for label, keys, transform_name in _FIELD_SPECS:

            if label in found:
                continue

            raw_value = _find(d, keys)

            if raw_value is None:
                continue

            transform = _TRANSFORMS.get(transform_name)
            value = transform(raw_value) if transform else raw_value

            if value in (None, "", [], {}):
                continue

            found[label] = str(value)

    return [
        (label, found[label])
        for label in _DISPLAY_ORDER
        if label in found
    ][:max_items]


# ==================================================================
# Ground-Truth Table Extraction
# ==================================================================

def _humanize(key: str) -> str:
    """'medicine_name' -> 'Medicine Name', 'id' -> 'ID'."""

    s = re.sub(r"(?<!^)(?=[A-Z])", "_", str(key))
    words = [w for w in re.split(r"[_\-]", s) if w]

    return " ".join(
        "ID" if w.lower() == "id" else w.capitalize()
        for w in words
    ) or str(key)


def _is_scalarish(value) -> bool:
    return not isinstance(value, (dict, list))


def _records_to_table(records, title=None, max_rows=50, max_cols=5):
    """One list of dict records -> one table dict, or None."""

    if not records or not all(isinstance(r, dict) for r in records):
        return None

    columns: list[str] = []
    seen = set()

    for item in records[: min(len(records), 10)]:
        for key, value in item.items():
            if key in seen or not _is_scalarish(value):
                continue
            seen.add(key)
            columns.append(key)

    if not columns:
        return None

    # "id" always leads when present.
    if "id" in columns:
        columns.remove("id")
        columns = ["id"] + columns

    columns = columns[:max_cols]
    labels = [_humanize(c) for c in columns]

    rows = [
        {labels[i]: item.get(col) for i, col in enumerate(columns)}
        for item in records[:max_rows]
    ]

    if len(records) > max_rows:
        title = f"{title or 'Records'} (showing {max_rows} of {len(records)})"

    return {"title": title, "columns": labels, "rows": rows}


def ground_truth_tables(result):
    """
    Builds every table for a response straight from the raw backend
    result — never through the LLM — so `id` and all values are
    exactly what the backend returned.

    - result is a list of records  -> one table
    - result is a dict             -> one table per non-empty list of
      records inside it (patient summary: encounters, medications,
      observations, diagnostic reports), titled from the key.
    """

    tables = []

    if isinstance(result, list):
        t = _records_to_table(result)
        if t:
            tables.append(t)

    elif isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, list) and value:
                t = _records_to_table(value, title=_humanize(key))
                if t:
                    tables.append(t)

    return tables