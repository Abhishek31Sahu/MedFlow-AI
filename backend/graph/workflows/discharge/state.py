"""
Discharge Workflow State
"""

from typing import Any

from graph.state import HospitalState

from graph.workflows.discharge.models.doctor_decision import (
    DoctorDecision
)

from graph.workflows.discharge.models.medication_review import (
    MedicationReview
)


class DischargeState(HospitalState):
    """
    Shared state for the Patient Discharge Workflow.
    """

    # ==========================================================
    # Extracted Input
    # ==========================================================

    workflow_data: dict

    # Example
    #
    # {
    #     "patient_name": "Hari Kumar",
    #     "reason": "Recovered",
    #     "follow_up": "After 7 days"
    # }

    # ==========================================================
    # Patient
    # ==========================================================

    resolved_patient: dict | None

    candidate_patients: list

    # ==========================================================
    # Encounter
    # ==========================================================

    active_encounter: dict | None

    encounter_id: str | None

    verified_encounter: dict | None

    # ==========================================================
    # Bed
    # ==========================================================

    bed_id: str | None

    bed: dict | None

    bed_status: str | None

    # ==========================================================
    # Bed Allocation
    # ==========================================================

    allocation_id: str | None

    allocation: dict | None

    allocation_status: str | None

    # ==========================================================
    # Medications
    # ==========================================================

    medications: list

    medication_review: MedicationReview | None

    doctor_decision: list[DoctorDecision]| None

    # ==========================================================
    # Workflow
    # ==========================================================

    workflow_status: str | None

    current_step: str | None

    workflow_results: list

    # ==========================================================
    # Final Result
    # ==========================================================

    result: Any