"""
Appointment API

HTTP endpoints for appointment management.
"""

from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.database import get_db
from core.security import (
    get_current_user,
    require_roles,
)

from models.enums import UserRole
from models.user import User

from services.appointment_service import (
    book_appointment,
    appointment_details,
    patient_appointment_history,
    practitioner_appointment_schedule,
    appointments_on_date,
    check_availability,
    check_patient_availability,
    reschedule_appointment,
    cancel_patient_appointment,
    check_in_patient,
    complete_patient_appointment,
    mark_appointment_no_show,
)


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


# ==========================================================
# REQUEST SCHEMAS
# ==========================================================

class CreateAppointmentRequest(BaseModel):
    patient_id: str = Field(
        ...,
        min_length=1,
    )

    # Optional for doctor because the backend should use
    # current_user.practitioner_id for a doctor.
    practitioner_id: Optional[str] = None

    start: str = Field(
        ...,
        min_length=1,
    )

    end: str = Field(
        ...,
        min_length=1,
    )

    reason: str = Field(
        default="General Consultation",
        min_length=1,
    )

    appointment_type: str = Field(
        default="ROUTINE",
        min_length=1,
    )

    description: Optional[str] = None


class RescheduleAppointmentRequest(BaseModel):
    new_start: str = Field(
        ...,
        min_length=1,
    )

    new_end: str = Field(
        ...,
        min_length=1,
    )


# ==========================================================
# BOOK APPOINTMENT
# ==========================================================

@router.post(
    "/",
)
def create_new_appointment(
    request: CreateAppointmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
        )
    ),
):
    """
    Create/book an appointment.

    Doctor:
        practitioner_id comes from current_user.practitioner_id

    Admin / Receptionist:
        practitioner_id comes from request.
    """

    # ------------------------------------------------------
    # Doctor identity must come from authenticated user
    # ------------------------------------------------------

    if current_user.role == UserRole.DOCTOR:

        practitioner_id = current_user.practitioner_id

        if not practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

    else:

        practitioner_id = request.practitioner_id

        if not practitioner_id:
            raise HTTPException(
                status_code=400,
                detail="practitioner_id is required.",
            )

    return book_appointment(
        db=db,
        patient_id=request.patient_id,
        practitioner_id=practitioner_id,
        start=request.start,
        end=request.end,
        reason=request.reason,
        appointment_type=request.appointment_type,
        description=request.description,
    )


# ==========================================================
# CHECK AVAILABILITY
# ==========================================================

@router.get(
    "/availability",
)
def get_availability(
    db: Session = Depends(get_db),
    practitioner_id: Optional[str] = Query(
        default=None,
    ),
    start: str = Query(
        ...,
    ),
    end: str = Query(
        ...,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    """
    Check whether a practitioner is available.

    Doctor:
        uses own practitioner_id.

    Other allowed roles:
        may specify practitioner_id.
    """

    if current_user.role == UserRole.DOCTOR:

        practitioner_id = current_user.practitioner_id

        if not practitioner_id:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Your user account is not linked "
                    "to a practitioner."
                ),
            )

    if not practitioner_id:

        raise HTTPException(
            status_code=400,
            detail="practitioner_id is required.",
        )

    return check_availability(
        db=db,
        practitioner_id=practitioner_id,
        start=start,
        end=end,
    )


# ==========================================================
# CHECK PATIENT AVAILABILITY
# ==========================================================

@router.get(
    "/patient-availability",
)
def get_patient_availability(
    
    patient_id: str = Query(
        ...,
    ),
    start: str = Query(
        ...,
    ),
    end: str = Query(
        ...,
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return check_patient_availability(
        patient_id=patient_id,
        start=start,
        end=end,
    )


# ==========================================================
# GET PATIENT APPOINTMENTS
# ==========================================================

@router.get(
    "/patient/{patient_id}",
)
def get_patient_appointments(
    patient_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return patient_appointment_history(
        patient_id
    )


# ==========================================================
# GET PRACTITIONER APPOINTMENTS
# ==========================================================

@router.get(
    "/practitioner/{practitioner_id}",
)
def get_practitioner_appointments(
    practitioner_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    # ------------------------------------------------------
    # Doctor can only view their own schedule
    # ------------------------------------------------------

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
                    "their own appointment schedule."
                ),
            )

    return practitioner_appointment_schedule(
        practitioner_id
    )


# ==========================================================
# GET APPOINTMENTS BY DATE
# ==========================================================

@router.get(
    "/date/{date}",
)
def get_date_appointments(
    date: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return appointments_on_date(
        date
    )


# ==========================================================
# GET SINGLE APPOINTMENT
# ==========================================================

@router.get(
    "/{appointment_id}",
)
def get_single_appointment(
    appointment_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return appointment_details(
        appointment_id
    )


# ==========================================================
# RESCHEDULE
# ==========================================================

@router.put(
    "/{appointment_id}/reschedule",
)
def reschedule_existing_appointment(
    appointment_id: str,
    request: RescheduleAppointmentRequest,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
        )
    ),
):
    """
    Reschedule an appointment.
    """

    return reschedule_appointment(
        appointment_id=appointment_id,
        new_start=request.new_start,
        new_end=request.new_end,
    )


# ==========================================================
# CANCEL
# ==========================================================

@router.put(
    "/{appointment_id}/cancel",
)
def cancel_existing_appointment(
    appointment_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.DOCTOR,
        )
    ),
):
    return cancel_patient_appointment(
        appointment_id
    )


# ==========================================================
# CHECK-IN
# ==========================================================

@router.put(
    "/{appointment_id}/check-in",
)
def check_in_appointment(
    appointment_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
            UserRole.NURSE,
        )
    ),
):
    return check_in_patient(
        appointment_id
    )


# ==========================================================
# COMPLETE APPOINTMENT
# ==========================================================

@router.put(
    "/{appointment_id}/complete",
)
def complete_appointment(
    appointment_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):
    return complete_patient_appointment(
        appointment_id
    )


# ==========================================================
# MARK NO-SHOW
# ==========================================================

@router.put(
    "/{appointment_id}/no-show",
)
def mark_appointment_as_no_show(
    appointment_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return mark_appointment_no_show(
        appointment_id
    )