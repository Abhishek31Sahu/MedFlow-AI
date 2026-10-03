"""
Discharge Workflow Router
"""

from graph.workflows.discharge.state import (
    DischargeState
)


# ==========================================================
# After Patient Resolution
# ==========================================================

def route_after_patient_resolution(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    if state.get("candidate_patients"):
        return "END"

    return "find_active_encounter"


# ==========================================================
# After Finding Encounter
# ==========================================================

def route_after_active_encounter(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "find_active_allocation"


# ==========================================================
# After Finding Active Allocation
# ==========================================================

def route_after_active_allocation(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "review_active_medications"


# ==========================================================
# After Medication Review
# ==========================================================

def route_after_medications(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    medications = state.get("medications", [])

    if not medications:
        return "complete_encounter"

    return "ai_medication_review"


# ==========================================================
# Resume After Doctor Approval
# ==========================================================

def route_after_doctor_approval(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "update_medications"


# ==========================================================
# After Updating Medications
# ==========================================================

def route_after_update_medications(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "complete_encounter"


# ==========================================================
# After Completing Encounter
# ==========================================================

def route_after_complete_encounter(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "release_bed"


# ==========================================================
# After Releasing Bed
# ==========================================================

def route_after_release_bed(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "complete_allocation"


# ==========================================================
# After Completing Allocation
# ==========================================================

def route_after_complete_allocation(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "verify_discharge"


# ==========================================================
# After Verification
# ==========================================================

def route_after_verification(
    state: DischargeState
):

    if state.get("error"):
        return "END"

    return "discharge_summary"