"""
Discharge API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Literal

from langgraph.types import Command

from core.security import require_roles
from models.enums import UserRole
from models.user import User

from services.graph_service import graph_service


router = APIRouter(
    prefix="/discharge",
    tags=["Discharge"],
)


# ==========================================================
# Doctor Decision
# ==========================================================

class DoctorDecisionRequest(BaseModel):

    medication_id: str

    medicine_name: str

    final_action: Literal[
        "continue",
        "stop",
        "modify",
    ]

    accepted_ai_recommendation: bool = True

    dosage: str | None = None

    frequency: str | None = None

    override_reason: str | None = None


# ==========================================================
# Medication Review Request
# ==========================================================

class MedicationReviewRequest(BaseModel):

    thread_id: str

    doctor_decision: list[DoctorDecisionRequest]


# ==========================================================
# Resume Discharge Workflow
# Admin + Doctor
# ==========================================================

@router.post("/medication-review")
async def medication_review(
    request: MedicationReviewRequest,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    # ------------------------------------------------------
    # Doctor must have a FHIR Practitioner ID
    # ------------------------------------------------------

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "No FHIR Practitioner ID is linked "
                    "to this doctor account."
                ),
            )

        practitioner_id = current_user.practitioner_id

    else:
        practitioner_id = current_user.practitioner_id

    # ------------------------------------------------------
    # LangGraph configuration
    # ------------------------------------------------------

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    # ------------------------------------------------------
    # Resume workflow
    # ------------------------------------------------------

    result = await graph_service.graph.ainvoke(
        Command(
            resume={
                "doctor_decision": [
                    decision.model_dump()
                    for decision in request.doctor_decision
                ]
            }
        ),
        config=config,
    )

    # ------------------------------------------------------
    # Handle another interrupt
    # ------------------------------------------------------

    if "__interrupt__" in result:

        interrupt = result["__interrupt__"][0]

        return {
            "success": True,
            "thread_id": request.thread_id,
            "interrupt": interrupt.value,
        }

    # ------------------------------------------------------
    # Final response
    # ------------------------------------------------------

    return {
        "success": True,
        "thread_id": request.thread_id,
        "result": result.get("result"),
        "response": result.get("response"),
        "interrupt": result.get("__interrupt__"),
    }