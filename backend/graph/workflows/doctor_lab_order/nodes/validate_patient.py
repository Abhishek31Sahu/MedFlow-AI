from graph.workflows.doctor_lab_order.state import DoctorLabOrderState

from services.encounter_service import find_active_encounter


async def validate_patient(
    state: DoctorLabOrderState,
) -> DoctorLabOrderState:
    """
    Validate resolved patient and fetch active encounter.
    """

    # ----------------------------------------------------
    # Patient must be resolved
    # ----------------------------------------------------

    patient = state.get("resolved_patient")

    if patient is None:
        return {
            **state,
            "error": "Patient not found.",
            "workflow_status": "FAILED",
            "current_step": "PATIENT_NOT_FOUND",
        }

    patient_id = patient["id"]

    # ----------------------------------------------------
    # Active Encounter
    # ----------------------------------------------------

    active_encounter = find_active_encounter(patient_id)

    if active_encounter is None:
        return {
            **state,
            "workflow_status": "IN_PROGRESS",
            "current_step": "PATIENT_VALIDATED",
        }

    return {
        **state,
        "encounter_id": active_encounter["id"],
        "active_encounter": active_encounter,
        "workflow_status": "IN_PROGRESS",
        "current_step": "PATIENT_VALIDATED",
    }