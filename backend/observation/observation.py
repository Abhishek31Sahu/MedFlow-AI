"""
Observation CRUD Operations
"""

from datetime import datetime

from fhir.client import fhir_client


# ==========================================================
# CREATE OBSERVATION
# ==========================================================

from datetime import datetime


from datetime import datetime, timezone

# fhir_client is your existing client, e.g.:
# from fhir.client import fhir_client


# ==============================================================
# Test name -> (LOINC code, display, default unit)
# Verify each code at loinc.org before relying on it.
# ==============================================================

LAB_CODES = {
    "blood group": ("882-1", "ABO and Rh group [Type] in Blood", ""),
    "hemoglobin": ("718-7", "Hemoglobin", "g/dL"),
    "total cholesterol": ("2093-3", "Total Cholesterol", "mg/dL"),
    "hdl cholesterol": ("2085-9", "HDL Cholesterol", "mg/dL"),
    "ldl cholesterol": ("13457-7", "LDL Cholesterol", "mg/dL"),
    "triglycerides": ("2571-8", "Triglycerides", "mg/dL"),
    "vldl cholesterol": ("13458-5", "VLDL Cholesterol", "mg/dL"),
    "total cholesterol / hdl ratio": (
        "9830-1",
        "Total Cholesterol / HDL Ratio",
        "ratio",
    ),
}


def resolve_lab_code(display: str, code: str | None = None):
    """
    Known test names get a fixed code/display/unit so the same test
    is always stored the same way. Unknown tests keep whatever the
    caller supplied.
    """

    hit = LAB_CODES.get((display or "").strip().lower())

    if hit:
        return hit

    return (code or display, display, "")


def build_value_field(value, unit: str | None) -> dict:
    """
    FHIR value[x]: numbers go in valueQuantity; text results
    (blood group, "Positive", "Reactive") go in valueString.
    """

    if isinstance(value, str):
        text = value.strip()

        try:
            value = float(text) if "." in text else int(text)
        except ValueError:
            return {"valueString": text}

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return {"valueString": str(value)}

    quantity = {"value": value}

    if unit:
        quantity["unit"] = unit

    return {"valueQuantity": quantity}


def create_observation(
    patient_id: str,
    code: str,
    display: str,
    value,
    unit: str = "",
    encounter_id: str | None = None,
    practitioner_id: str | None = None,
    category: str = "laboratory",
    interpretation: str | None = None,
    note: str | None = None,
    low_reference=None,
    high_reference=None,
):

    known_code, known_display, default_unit = resolve_lab_code(display, code)

    unit = unit or default_unit

    now = datetime.now(timezone.utc).isoformat()

    resource = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": category,
                        "display": category.capitalize(),
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": known_code,
                    "display": known_display,
                }
            ],
            "text": known_display,
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": now,
        "issued": now,
    }

    resource.update(build_value_field(value, unit))

    if encounter_id:
        resource["encounter"] = {"reference": f"Encounter/{encounter_id}"}

    if practitioner_id:
        resource["performer"] = [
            {"reference": f"Practitioner/{practitioner_id}"}
        ]

    if interpretation:
        resource["interpretation"] = [{"text": interpretation}]

    # Reference ranges only make sense for numeric results.
    if "valueQuantity" in resource and (
        low_reference is not None or high_reference is not None
    ):
        ref = {}

        if low_reference is not None:
            ref["low"] = {"value": low_reference}

        if high_reference is not None:
            ref["high"] = {"value": high_reference}

        resource["referenceRange"] = [ref]

    if note:
        resource["note"] = [{"text": note}]

    return fhir_client.create("Observation", resource)

# ==========================================================
# READ
# ==========================================================

def get_observation_value(resource: dict):
    """
    Returns (value, unit) for an Observation resource.
    Numeric results live in valueQuantity; text results
    (blood group, "Positive", ...) live in valueString.
    """
    if "valueQuantity" in resource:
        q = resource["valueQuantity"]
        return q.get("value"), q.get("unit", "")

    if "valueString" in resource:
        return resource["valueString"], ""

    return None, ""


def get_observation(
    observation_id
):

    return fhir_client.read(
        "Observation",
        observation_id
    )


# ==========================================================
# GET PATIENT OBSERVATIONS
# ==========================================================

def get_patient_observations(patient_id):

    return fhir_client.search(
        "Observation",
        {
            "patient": patient_id,
            "_count": 1000,
            "_sort": "-date"
        }
    )


# ==========================================================
# SEARCH BY TEST NAME
# ==========================================================

def get_observation_by_test(
    patient_id,
    test_name
):

    bundle = get_patient_observations(
        patient_id
    )

    if "entry" not in bundle:
        return []

    observations = []

    for entry in bundle["entry"]:

        resource = entry["resource"]

        name = (
            resource
            .get("code", {})
            .get("text", "")
        )

        if name.lower() == test_name.lower():

            observations.append(resource)

    return observations


# ==========================================================
# LATEST OBSERVATION
# ==========================================================

def latest_observation(
    patient_id,
    test_name
):

    observations = get_observation_by_test(
        patient_id,
        test_name
    )

    if not observations:
        return None

    observations.sort(

        key=lambda x:
        x["effectiveDateTime"],

        reverse=True
    )

    return observations[0]


# ==========================================================
# UPDATE
# ==========================================================

def update_observation(
    observation_id,
    value
):

    observation = get_observation(
        observation_id
    )

    observation["valueQuantity"]["value"] = value

    return fhir_client.update(
        "Observation",
        observation_id,
        observation
    )


# ==========================================================
# DELETE
# ==========================================================

def delete_observation(
    observation_id
):

    return fhir_client.delete(
        "Observation",
        observation_id
    )


# ==========================================================
# PRINT
# ==========================================================

def print_observation(
    observation
):

    print("=" * 60)

    print(
        "Observation ID:",
        observation["id"]
    )

    print(
        "Test:",
        observation["code"]["text"]
    )

    print(
        "Value:",
        observation["valueQuantity"]["value"]
    )

    print(
        "Unit:",
        observation["valueQuantity"]["unit"]
    )

    print(
        "Date:",
        observation["effectiveDateTime"]
    )

    print("=" * 60)