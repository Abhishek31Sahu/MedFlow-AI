"""
Transfer Workflow State
"""

from typing import Any

from graph.state import (
    HospitalState
)


class TransferState(HospitalState):
    """
    Shared state for the Patient Transfer Workflow.
    """

    # ==========================================================
    # Extracted Input
    # ==========================================================

    user_query: str
    workflow_data: dict

    # Example:
    # {
    #     "patient_name": "Hari Kumar",
    #     "destination_location": "ICU",
    #     "reason": "Condition worsened"
    # }

    # ==========================================================
    # Patient
    # ==========================================================

    resolved_patient: dict | None
    candidate_patients: list[dict]

    # ==========================================================
    # Encounter
    # ==========================================================

    active_encounter: dict | None
    verified_encounter: dict | None
    encounter_id: str | None

    # ==========================================================
    # Current Location
    # ==========================================================

    current_location_id: str | None
    current_location_name: str | None

    # ==========================================================
    # Patient Requirements
    # ==========================================================

    patient_requirements: dict

    # ==========================================================
    # Bed Recommendation
    # ==========================================================

    recommended_beds: list[dict]

    selected_bed: dict | None
    assigned_bed: dict | None

    allocation_id : str | None
    allocation_status: str | None
    allocation : dict | None
    # ==========================================================
    # Doctor Decision
    # ==========================================================

    bed_decision: dict | None
    # Example:
    # {
    #     "action": "select" | "manual" | "reject",
    #     "selected_bed": {...},
    #     "bed_id": "...",
    #     "reason": "..."
    # }

    # ==========================================================
    # FHIR Encounter
    # ==========================================================

    updated_encounter: dict | None

    # ==========================================================
    # Workflow
    # ==========================================================

    workflow_status: str | None
    current_step: str | None
    workflow_results: list
    error : str | None
    # ==========================================================
    # Final Result
    # ==========================================================

    result: Any