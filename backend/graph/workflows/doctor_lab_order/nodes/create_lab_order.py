from graph.workflows.doctor_lab_order.state import DoctorLabOrderState

from schemas.laboratory import (
    CreateLabOrderRequest,
    LabTest,
)

from services.laboratory_service import LaboratoryService
from database.database import SessionLocal


def create_lab_order(
    state: DoctorLabOrderState,
) -> DoctorLabOrderState:
    """
    Create laboratory order(s).
    """

    patient = state["resolved_patient"]

    workflow_data = state["workflow_data"]

    # Create synchronous database session
    db = SessionLocal()
    
    if state.get("practitioner_id") is None:
                    return {
                        **state,
                        "error": "Practitioner ID is missing.",
                        "workflow_status": "FAILED",
                        "current_step": "PRACTITIONER_ID_MISSING",
                    }

    try:

        service = LaboratoryService(db)

        request = CreateLabOrderRequest(

            patient_id=patient["id"],

            encounter_id=state.get("encounter_id"),
        
            practitioner_id=state["practitioner_id"],

            tests=[
                LabTest(
                    code=test.get("code"),
                    name=test["name"],
                )
                for test in workflow_data["tests"]
            ],

            priority=workflow_data["priority"],

            clinical_note=workflow_data.get(
                "clinical_note"
            ),
        )

        # Synchronous service call
        orders = service.create_lab_order(request)
        # print("Orders created:", orders)
        for order in orders:
            print(
                f"Order ID: {order.id}, "
                f"Service Request ID: {order.service_request_id}, "
                f"Test Name: {order.test_name}"
            )
        laboratory_orders = [
            {
                "id": str(order.id),
                "service_request_id": order.service_request_id,
                "patient_id": order.patient_id,
                "encounter_id": order.encounter_id,
                "practitioner_id": order.practitioner_id,
                "technician_id": order.technician_id,
                "test_code": order.test_code,
                "test_name": order.test_name,
                "priority": (
                    order.priority.value
                    if hasattr(order.priority, "value")
                    else order.priority
                ),
                "status": (
                    order.status.value
                    if hasattr(order.status, "value")
                    else order.status
                ),
                "sample_status": (
                    order.sample_status.value
                    if hasattr(order.sample_status, "value")
                    else order.sample_status
                ),
                "clinical_note": order.clinical_note,
                "ordered_at": (
                    order.ordered_at.isoformat()
                    if order.ordered_at
                    else None
                ),
                "completed_at": (
                    order.completed_at.isoformat()
                    if order.completed_at
                    else None
                ),
            }
            for order in orders
        ]
        state["laboratory_orders"] = laboratory_orders
        state["workflow_status"]="COMPLETED"
        state["current_step"]="LAB_ORDER_CREATED"
        return state

    finally:
        db.close()