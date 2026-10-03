"""
Admission Workflow Router
"""

from graph.workflows.admission.state import AdmissionState


# ==========================================================
# After Patient Resolution
# ==========================================================

def route_after_patient_resolution(
    state: AdmissionState
):

    if state.get("error"):
        return "admission_summary"

    if state.get("candidate_patients"):
        return "admission_summary"

    return "check_active_encounter"


# ==========================================================
# After Active Encounter Check
# ==========================================================

def route_after_active_encounter(
    state: AdmissionState
):

    if state.get("active_encounter"):

        state["error"] = (
            "Patient already has an active encounter."
        )

        return "admission_summary"

    return "build_patient_requirements"


# ==========================================================
# After Reserve Bed
# ==========================================================

def route_after_allocate_bed(
    state: AdmissionState
):

    if state.get("error"):
        return "admission_summary"

    return "create_encounter"


# ==========================================================
# After Encounter Creation
# ==========================================================

def route_after_create_encounter(
    state: AdmissionState
):

    if state.get("error") or not state.get("encounter_id"):
        return "release_reserved_bed"

    return "assign_bed"


# ==========================================================
# After Allocation
# ==========================================================

def route_after_create_allocation(
    state: AdmissionState
):

    if state.get("error"):
        return "release_reserved_bed"

    return "admission_summary"


# ==========================================================
# After Release Reserved Bed
# ==========================================================

def route_after_release_reserved_bed(
    state: AdmissionState
):

    return "admission_summary"