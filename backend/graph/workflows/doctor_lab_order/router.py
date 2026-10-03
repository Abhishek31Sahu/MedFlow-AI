from graph.workflows.doctor_lab_order.state import DoctorLabOrderState


def workflow_router(state: DoctorLabOrderState) -> str:
    """
    Route workflow based on status.
    """
    if state.get("workflow_status") == "FAILED":
        return "response"

    return "next"