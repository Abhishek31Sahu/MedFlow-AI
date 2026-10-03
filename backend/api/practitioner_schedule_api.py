"""
Practitioner Schedule API

Manage recurring working schedules for practitioners.
"""

from datetime import time
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session

from database.database import get_db
from core.security import require_roles
from models.enums import UserRole
from models.user import User

from services.practitioner_schedule_service import (
    create_schedule,
    get_practitioner_schedule,
    get_schedule_for_day,
    get_today_schedule,
    is_practitioner_working_today,
    update_schedule,
    delete_schedule,
)


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/practitioner-schedules",
    tags=["Practitioner Schedules"],
)


# ==========================================================
# REQUEST SCHEMAS
# ==========================================================

class CreateScheduleRequest(BaseModel):

    practitioner_id: str = Field(
        ...,
        min_length=1,
    )

    day_of_week: str = Field(
        ...,
        min_length=1,
    )

    start_time: time

    end_time: time


class UpdateScheduleRequest(BaseModel):

    start_time: Optional[time] = None

    end_time: Optional[time] = None

    is_active: Optional[bool] = None


# ==========================================================
# RESPONSE FORMATTER
# ==========================================================

def _format_schedule(schedule):

    return {
        "id": schedule.id,
        "practitioner_id": schedule.practitioner_id,
        "day_of_week": schedule.day_of_week,
        "start_time": (
            schedule.start_time.isoformat()
            if schedule.start_time
            else None
        ),
        "end_time": (
            schedule.end_time.isoformat()
            if schedule.end_time
            else None
        ),
        "is_active": schedule.is_active,
    }


# ==========================================================
# CREATE SCHEDULE
# ==========================================================

@router.post(
    "/",
)
def create_practitioner_schedule(
    request: CreateScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    """
    Admin creates a working schedule for a practitioner.
    """

    schedule = create_schedule(
        db=db,
        practitioner_id=request.practitioner_id,
        day_of_week=request.day_of_week,
        start_time=request.start_time,
        end_time=request.end_time,
    )

    return {
        "success": True,
        "message": "Practitioner schedule created successfully.",
        "schedule": _format_schedule(schedule),
    }


# ==========================================================
# GET FULL PRACTITIONER SCHEDULE
# ==========================================================

@router.get(
    "/practitioner/{practitioner_id}",
)
def get_practitioner_schedule_endpoint(
    practitioner_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    """
    Return all active working schedules for a practitioner.

    A doctor can only view their own schedule.
    """

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

        if practitioner_id != current_user.practitioner_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Doctors can only view "
                    "their own schedule."
                ),
            )

    schedules = get_practitioner_schedule(
        db=db,
        practitioner_id=practitioner_id,
    )

    return {
        "practitioner_id": practitioner_id,
        "schedules": [
            _format_schedule(schedule)
            for schedule in schedules
        ],
    }


# ==========================================================
# GET SCHEDULE FOR SPECIFIC DAY
# ==========================================================

@router.get(
    "/practitioner/{practitioner_id}/day/{day_of_week}",
)
def get_schedule_for_day_endpoint(
    practitioner_id: str,
    day_of_week: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    """
    Example:

    GET
    /practitioner-schedules/practitioner/2001/day/monday
    """

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

        if practitioner_id != current_user.practitioner_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Doctors can only view "
                    "their own schedule."
                ),
            )

    schedules = get_schedule_for_day(
        db=db,
        practitioner_id=practitioner_id,
        day_of_week=day_of_week,
    )

    return {
        "practitioner_id": practitioner_id,
        "day_of_week": day_of_week.lower(),
        "schedules": [
            _format_schedule(schedule)
            for schedule in schedules
        ],
    }


# ==========================================================
# GET TODAY'S SCHEDULE
# ==========================================================

@router.get(
    "/practitioner/{practitioner_id}/today",
)
def get_today_schedule_endpoint(
    practitioner_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    """
    Get today's working schedule for a practitioner.
    """

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

        if practitioner_id != current_user.practitioner_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Doctors can only view "
                    "their own schedule."
                ),
            )

    schedules = get_today_schedule(
        db=db,
        practitioner_id=practitioner_id,
    )

    return {
        "practitioner_id": practitioner_id,
        "working_today": len(schedules) > 0,
        "schedules": [
            _format_schedule(schedule)
            for schedule in schedules
        ],
    }


# ==========================================================
# CHECK WHETHER DOCTOR WORKS TODAY
# ==========================================================

@router.get(
    "/practitioner/{practitioner_id}/working-today",
)
def practitioner_working_today(
    practitioner_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    """
    Simple endpoint used by the appointment
    availability workflow.
    """

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

        if practitioner_id != current_user.practitioner_id:
            raise HTTPException(
                status_code=403,
                detail=(
                    "Doctors can only access "
                    "their own schedule."
                ),
            )

    result = is_practitioner_working_today(
        db=db,
        practitioner_id=practitioner_id,
    )

    return {
        "practitioner_id": practitioner_id,
        "working_today": result["working_today"],
        "day": result["day"],
        "schedule": [
            _format_schedule(schedule)
            for schedule in result["schedule"]
        ],
    }


# ==========================================================
# UPDATE SCHEDULE
# ==========================================================

@router.put(
    "/{schedule_id}",
)
def update_practitioner_schedule(
    schedule_id: str,
    request: UpdateScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    """
    Admin updates a practitioner schedule.
    """

    schedule = update_schedule(
        db=db,
        schedule_id=schedule_id,
        start_time=request.start_time,
        end_time=request.end_time,
        is_active=request.is_active,
    )

    return {
        "success": True,
        "message": "Practitioner schedule updated successfully.",
        "schedule": _format_schedule(schedule),
    }


# ==========================================================
# DELETE / DEACTIVATE SCHEDULE
# ==========================================================

@router.delete(
    "/{schedule_id}",
)
def delete_practitioner_schedule(
    schedule_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    """
    Soft-delete a practitioner schedule.
    """

    return delete_schedule(
        db=db,
        schedule_id=schedule_id,
    )