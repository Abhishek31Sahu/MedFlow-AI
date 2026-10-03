from graph.workflows.doctor_lab_order.state import DoctorLabOrderState


async def response(
    state: DoctorLabOrderState,
) -> DoctorLabOrderState:
    """
    Generate the final workflow response.
    """

    # -----------------------------
    # Failure Response
    # -----------------------------
    if state.get("workflow_status") == "FAILED":
        print("Workflow failed. Generating failure response.")

        state["result"] = {
            "success": False,
            "message": state.get("error", "Laboratory workflow failed."),
            "current_step": state.get("current_step"),
        }

        return state

    # -----------------------------
    # Success Response
    # -----------------------------
    patient = state["resolved_patient"]
    orders = state["laboratory_orders"]
    for order in orders:
        print(
                    f"Order ID: {order['id']}, "
                    f"Service Request ID: {order['service_request_id']}, "
                    f"Test Name: {order['test_name']}"
                )
    tests = [
        {
            "service_request_id": order['service_request_id'],
            "test_name": order['test_name'],
        }
        for order in orders
    ]

    state["result"] = {
        "success": True,
        "message": "Laboratory order created successfully.",
        "patient": {
            "id": patient["id"],
            "name": patient["name"],
        },
        "total_tests": len(orders),
        "tests": tests,
        "summary": (
            f"Laboratory order(s) successfully created for "
            f"{patient['name']}."
        ),
    }

    return state