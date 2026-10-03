from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from pydantic import BaseModel

from core.security import require_roles
from models.enums import UserRole
from models.user import User
from services.graph_service import graph_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


# ==========================================================
# AI CHAT REQUEST
# ==========================================================

class AIRequest(BaseModel):
    query: str
    thread_id: str | None = None


# ==========================================================
# AI CHAT
# Admin + Doctor
# ==========================================================

@router.post("/chat")
async def ai_chat(
    request: AIRequest,
    current_user: User = Depends(
    require_roles(
        UserRole.ADMIN,
        UserRole.DOCTOR,
        UserRole.NURSE,
        UserRole.RECEPTIONIST,
        UserRole.LAB_TECHNICIAN,
        UserRole.PHARMACIST,
    )
)
):
    # ------------------------------------------------------
    # Doctor must have a linked FHIR Practitioner
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

    # ------------------------------------------------------
    # Admin
    #
    # Admin does not normally represent a clinical
    # Practitioner. Therefore AI clinical workflows
    # require a practitioner_id from the request only
    # if you decide to support admin acting on behalf
    # of a doctor.
    # ------------------------------------------------------

    
    practitioner_id = current_user.practitioner_id

    user_id = str(current_user.id)

    user_role = current_user.role


    # ------------------------------------------------------
    # Thread
    # ------------------------------------------------------
    print(request.model_dump())
    thread_id = request.thread_id or str(uuid4())

    # ------------------------------------------------------
    # Initial LangGraph State
    # ------------------------------------------------------

    state = {
        "user_query": request.query,
        "messages": [
            HumanMessage(content=request.query)
        ],
        "user_id": user_id,
        "user_role": user_role,
        "authorization_denied": False,
        "planner": None,
        "practitioner_id": practitioner_id,
        "result": None,
        "error": None,
        "response": None,
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    # ------------------------------------------------------
    # Execute Graph
    # ------------------------------------------------------

    result = await graph_service.graph.ainvoke(
        state,
        config=config,
    )

    # ------------------------------------------------------
    # Handle Interrupt
    # ------------------------------------------------------

    if "__interrupt__" in result:

        interrupt = result["__interrupt__"][0]

        return {
            "success": True,
            "thread_id": thread_id,
            "interrupt": interrupt.value,
        }

    # ------------------------------------------------------
    # Normal Response
    # ------------------------------------------------------

    return {
        "success": True,
        "thread_id": thread_id,
        "response": result.get("response"),
        "interrupt": result.get("__interrupt__"),
    }


# ==========================================================
# RESOLVE PATIENT DURING ADMISSION
# Doctor + Admin
# ==========================================================

class ResumeRequest(BaseModel):

    thread_id: str

    selected_patient_id: str


@router.post("/admission/resolvePatient")
async def resume(
    request: ResumeRequest,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    # ------------------------------------------------------
    # Inspect checkpoint
    # ------------------------------------------------------

    state = await graph_service.graph.aget_state(
        config
    )

    print("========== CHECKPOINT ==========")
    print(state)
    print("================================")

    # ------------------------------------------------------
    # Resume LangGraph
    # ------------------------------------------------------

    result = await graph_service.graph.ainvoke(
        Command(
            resume={
                "patient_id": request.selected_patient_id
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
        "response": result.get("response"),
        "interrupt": result.get("__interrupt__"),
    }


# ==========================================================
# BED SELECTION
# Doctor + Admin
# ==========================================================

class BedSelectionRequest(BaseModel):

    thread_id: str

    action: Literal[
        "select",
        "manual",
        "reject",
    ]

    selected_bed: dict | None = None

    bed_id: str | None = None

    reason: str | None = None


@router.post("/admission/bed-selection")
async def bed_selection(
    request: BedSelectionRequest,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    print(request.model_dump())

    # ------------------------------------------------------
    # Inspect checkpoint
    # ------------------------------------------------------

    state = await graph_service.graph.aget_state(
        config
    )

    print("========== CHECKPOINT ==========")
    print(state)
    print("================================")

    # ------------------------------------------------------
    # Resume workflow
    # ------------------------------------------------------

    result = await graph_service.graph.ainvoke(
        Command(
            resume={
                "action": request.action,
                "selected_bed": request.selected_bed,
                "bed_id": request.bed_id,
                "reason": request.reason,
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
        "response": result.get("response"),
        "interrupt": result.get("__interrupt__"),
    }
    
    
    from pydantic import BaseModel


class AppointmentConfirmationRequest(BaseModel):
    thread_id: str
    confirmed: bool
    
@router.post("/appointment/confirm")
async def confirm_appointment(request: AppointmentConfirmationRequest,current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),):
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = await graph_service.graph.ainvoke(
        Command(
            resume={
                "confirmed": request.confirmed
            }
        ),
        config=config,
    )

    return result