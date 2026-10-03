"""
Transfer Router
"""

from graph.workflows.transfer.state import TransferState


# --------------------------------------------------
# Resolve Patient
# --------------------------------------------------

def route_resolve_patient(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"



# --------------------------------------------------
# Verify Encounter
# --------------------------------------------------

def route_verify_encounter(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"


# --------------------------------------------------
# Build Patient Requirements
# --------------------------------------------------

def route_build_patient_requirements(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"


# --------------------------------------------------
# Recommend Bed
# --------------------------------------------------

def route_recommend_bed(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"


# --------------------------------------------------
# Select Bed
# --------------------------------------------------

def route_select_bed(state: TransferState):

    if state.get("error"):
        return "error"

    decision = state.get("bed_decision")

    if decision is None:
        return "error"

    action = decision["action"]

    if action == "manual":
        return "manual"

    if action == "reject":
        return "reject"

    return "success"


# --------------------------------------------------
# Validate Manual Bed
# --------------------------------------------------

def route_validate_manual_bed(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"

# complete allocation

def route_find_active_allocation(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"

def route_complete_allocation(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"
# --------------------------------------------------
# Transfer Patient
# --------------------------------------------------

def route_transfer_patient(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"


# --------------------------------------------------
# Update Encounter
# --------------------------------------------------

def route_update_encounter(state: TransferState):

    if state.get("error"):
        return "error"

    return "success"

