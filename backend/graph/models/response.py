"""
Standardized Response Schema
=============================

Every specialist agent (patient, encounter, medication, observation,
appointment, summary) and every multi-step clinical workflow
(admission, discharge, transfer, lab order, appointment booking /
reschedule) funnels through the single `response_agent` node before
reaching the doctor. That node always emits THIS exact shape.

The frontend renders ONE component (e.g. <ResponseCard />) against
this schema, so the UI a doctor sees never changes shape depending on
which agent or workflow produced it — only the content inside changes.

Design intent: a doctor should be able to tell, in under two seconds,
whether something succeeded, what it was about, and the two or three
facts that matter (patient, bed, drug + dose, result value, etc.)
without reading a paragraph.
"""

from typing import Literal

from pydantic import BaseModel, Field


# ==============================================================
# Building blocks
# ==============================================================

class Highlight(BaseModel):
    """
    One quick-scan fact rendered as a label/value chip, e.g.
    {"label": "Patient", "value": "John Doe (P-0234)"}.

    Keep these short — this is the "glanceable" layer, not the
    place for paragraphs. 3-6 highlights per response is the sweet
    spot; more than that belongs in `table` or `data` instead.
    """

    label: str

    value: str

    # Lets the UI draw attention (amber/red chip) without the
    # frontend having to parse clinical meaning out of free text.
    emphasis: Literal["normal", "warning", "critical"] = "normal"


class ResponseTable(BaseModel):
    """
    Used whenever the backend result is a list of similar records —
    active medications, observation history, a patient's
    appointments, candidate/recommended beds, etc. Column order is
    the render order; keep it small (3-5 columns) so it stays
    readable on a clinical workstation or tablet.
    """

    # Optional heading, e.g. "Medications" / "Observations" — lets one
    # response carry several tables (patient summary has four lists).
    title: str | None = None

    columns: list[str]

    # Each row is keyed by the exact strings in `columns`.
    rows: list[dict]


class WorkflowInfo(BaseModel):
    """
    Present only when a multi-step clinical workflow is involved
    (admission, discharge, transfer, lab order, appointment
    booking/reschedule). `status` mirrors HospitalState.workflow_status
    verbatim so the frontend and backend never disagree about state.
    """

    name: str

    status: str

    step: str | None = None

    missing_fields: list[str] = Field(default_factory=list)


# ==============================================================
# What the LLM is allowed to fill in
# ==============================================================

class ResponseContent(BaseModel):
    """
    The ONLY thing the LLM produces. Deliberately narrow: no
    success/status/category fields here, because those are ground
    truth derived in code from the backend result and workflow
    state — never left to the model to guess or restate, so they
    can always be trusted 1:1 by the frontend.
    """

    title: str

    message: str

    highlights: list[Highlight] = Field(default_factory=list)

    # Short reply chips a doctor can tap — only meaningful when
    # status == "action_required" (a workflow is waiting on input)
    # or to confirm/cancel a pending step. Empty otherwise.
    suggested_replies: list[str] = Field(default_factory=list)


# ==============================================================
# What actually reaches the frontend
# ==============================================================

class ResponseOutput(BaseModel):
    """
    The single, permanently-fixed response contract. `response_agent`
    is the only place in the codebase allowed to construct this.
    """

    # ---- Control fields: set deterministically in response_agent,
    # ---- from state["error"] / state["workflow_status"], never by
    # ---- the LLM -------------------------------------------------
    success: bool

    status: Literal["success", "error", "action_required", "in_progress"]

    # Stable machine-readable source identifier: the specialist
    # agent name ("patient", "medication", ...) or the active
    # workflow name ("patient_admission", "lab_order", ...).
    # The frontend can use this for an icon lookup, but must NOT
    # change layout based on it — layout is fixed by `status`.
    category: str

    # ---- Content fields: produced by the LLM, constrained to
    # ---- ResponseContent above -----------------------------------
    title: str

    message: str

    highlights: list[Highlight] = Field(default_factory=list)

    # Built deterministically from the raw backend result in code
    # (never by the LLM), so IDs and values are always exact.
    tables: list[ResponseTable] = Field(default_factory=list)

    suggested_replies: list[str] = Field(default_factory=list)

    # ---- Raw fallback so nothing the backend returned is ever
    # ---- lost, even if the LLM summarized it -----------------------
    data: dict | list | None = None

    # ---- Present only for workflow-driven responses -----------------
    workflow: WorkflowInfo | None = None