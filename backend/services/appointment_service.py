"""
Appointment Service

Business logic for appointment management.
"""

from datetime import datetime, timedelta

from fastapi import HTTPException, status

from appointment.appointment import (
    create_appointment,
    get_appointment,
    get_patient_appointments,
    get_practitioner_appointments,
    get_appointments_by_date,
    print_appointment,
    update_appointment,
    cancel_appointment,
    checkin_appointment,
    complete_appointment,
    mark_no_show,
    get_practitioner_appointments_between,
    get_patient_appointments_between,
    get_patient_id_from_appointment,
    get_practitioner_id_from_appointment,
)

from services.practitioner_schedule_service import (
    get_schedule_for_day,
)

# ==========================================================
# CHECK PRACTITIONER AVAILABILITY
# ==========================================================

def check_availability(
    db,
    practitioner_id: str,
    start: str,
    end: str,
    exclude_appointment_id: str | None = None,
):
    """
    Check whether a practitioner is available for a
    requested appointment time.

    Checks:

    1. Valid time range
    2. Practitioner working schedule
    3. Existing FHIR appointments
    """

    # ------------------------------------------------------
    # Parse requested datetime
    # ------------------------------------------------------

    try:
        start_dt = datetime.fromisoformat(
            start.replace("Z", "+00:00")
        )

        end_dt = datetime.fromisoformat(
            end.replace("Z", "+00:00")
        )

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid start or end datetime.",
        )

    # ------------------------------------------------------
    # Validate range
    # ------------------------------------------------------

    if end_dt <= start_dt:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    # ------------------------------------------------------
    # Determine requested day
    # ------------------------------------------------------

    day_of_week = start_dt.strftime(
        "%A"
    ).lower()

    # ------------------------------------------------------
    # Get doctor's schedule for that day
    # ------------------------------------------------------

    schedules = get_schedule_for_day(
        db=db,
        practitioner_id=practitioner_id,
        day_of_week=day_of_week,
    )

    # ------------------------------------------------------
    # Doctor does not work that day
    # ------------------------------------------------------

    if not schedules:

        return {
            "available": False,
            "working_today": False,
            "reason": (
                "Practitioner is not scheduled "
                f"to work on {day_of_week}."
            ),
            "practitioner_id": practitioner_id,
            "day": day_of_week,
            "requested_start": start,
            "requested_end": end,
            "conflicts": [],
        }

    # ------------------------------------------------------
    # Check whether requested slot is inside working hours
    # ------------------------------------------------------

    requested_start_time = start_dt.time()
    requested_end_time = end_dt.time()

    inside_working_hours = False
    matched_schedule = None

    for schedule in schedules:

        schedule_start = schedule.start_time
        schedule_end = schedule.end_time

        if (
            requested_start_time >= schedule_start
            and requested_end_time <= schedule_end
        ):
            inside_working_hours = True
            matched_schedule = schedule
            break

    # ------------------------------------------------------
    # Requested time is outside doctor's working hours
    # ------------------------------------------------------

    if not inside_working_hours:

        return {
            "available": False,
            "working_today": True,
            "reason": (
                "Requested time is outside "
                "the practitioner's working hours."
            ),
            "practitioner_id": practitioner_id,
            "day": day_of_week,
            "requested_start": start,
            "requested_end": end,

            "working_hours": [
                {
                    "start_time": (
                        schedule.start_time.isoformat()
                    ),
                    "end_time": (
                        schedule.end_time.isoformat()
                    ),
                }
                for schedule in schedules
            ],

            "conflicts": [],
        }

    # ------------------------------------------------------
    # Check existing appointments
    # ------------------------------------------------------

    conflicts = get_practitioner_appointments_between(
    practitioner_id=practitioner_id,
    start=start,
    end=end,
)

    if exclude_appointment_id:
        conflicts = [
            appointment
            for appointment in conflicts
            if appointment.get("id") != exclude_appointment_id
        ]

    # ------------------------------------------------------
    # Appointment conflict exists
    # ------------------------------------------------------

    if conflicts:

        return {
            "available": False,
            "working_today": True,
            "reason": (
                "Practitioner already has "
                "an appointment during this time."
            ),
            "practitioner_id": practitioner_id,
            "day": day_of_week,
            "requested_start": start,
            "requested_end": end,

            "working_hours": [
                {
                    "start_time": (
                        schedule.start_time.isoformat()
                    ),
                    "end_time": (
                        schedule.end_time.isoformat()
                    ),
                }
                for schedule in schedules
            ],

            "conflicts": [
                {
                    "id": appointment.get("id"),
                    "start": appointment.get("start"),
                    "end": appointment.get("end"),
                    "status": appointment.get("status"),
                }
                for appointment in conflicts
            ],
        }

    # ------------------------------------------------------
    # AVAILABLE
    # ------------------------------------------------------

    return {
        "available": True,
        "working_today": True,
        "reason": "Practitioner is available.",
        "practitioner_id": practitioner_id,
        "day": day_of_week,
        "requested_start": start,
        "requested_end": end,

        "working_hours": {
            "start_time": (
                matched_schedule.start_time.isoformat()
            ),
            "end_time": (
                matched_schedule.end_time.isoformat()
            ),
        },

        "conflicts": [],
    }
# ==========================================================
# VALIDATE DATE/TIME
# ==========================================================

def _validate_time_range(
    start: str,
    end: str,
):
    try:
        start_dt = datetime.fromisoformat(
            start.replace("Z", "+00:00")
        )

        end_dt = datetime.fromisoformat(
            end.replace("Z", "+00:00")
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid start or end datetime.",
        )

    if end_dt <= start_dt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment end time must be after start time.",
        )

    return start_dt, end_dt




# ==========================================================
# CHECK PATIENT AVAILABILITY
# ==========================================================

def check_patient_availability(
    patient_id: str,
    start: str,
    end: str,
):
    """
    A patient should not have two overlapping appointments.
    """

    _validate_time_range(
        start,
        end,
    )

    conflicts = get_patient_appointments_between(
        patient_id=patient_id,
        start=start,
        end=end,
    )

    return {
        "available": len(conflicts) == 0,
        "conflicts": conflicts,
    }


# ==========================================================
# BOOK APPOINTMENT
# ==========================================================
from sqlalchemy.orm import Session

def book_appointment(
    db: Session,
    patient_id: str,
    practitioner_id: str,
    start: str,
    end: str,
    reason: str = "General Consultation",
    appointment_type: str = "ROUTINE",
    description: str | None = None,
):
    """
    Complete appointment booking workflow.

    1. Validate time
    2. Check practitioner schedule + doctor conflict
    3. Check patient conflict
    4. Create appointment
    """

    # ------------------------------------------------------
    # Validate requested time
    # ------------------------------------------------------

    _validate_time_range(start, end)

    # ------------------------------------------------------
    # Check practitioner availability
    # ------------------------------------------------------
    # This checks:
    #   - Is practitioner working that day?
    #   - Is requested time inside working hours?
    #   - Does practitioner already have an appointment?
    # ------------------------------------------------------

    availability = check_availability(
        db=db,
        practitioner_id=practitioner_id,
        start=start,
        end=end,
    )

    if not availability["available"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=availability["reason"],
        )

    # ------------------------------------------------------
    # Check patient conflict
    # ------------------------------------------------------

    patient_conflicts = get_patient_appointments_between(
        patient_id=patient_id,
        start=start,
        end=end,
    )

    if patient_conflicts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Patient already has an appointment "
                "during the requested time."
            ),
        )

    # ------------------------------------------------------
    # Create FHIR Appointment
    # ------------------------------------------------------

    appointment = create_appointment(
        patient_id=patient_id,
        practitioner_id=practitioner_id,
        start=start,
        end=end,
        reason=reason,
        appointment_type=appointment_type,
        description=description,
    )

    return {
        "success": True,
        "message": "Appointment booked successfully.",
        "appointment_id": appointment["id"],
        "appointment": appointment,
    }

# ==========================================================
# GET APPOINTMENT
# ==========================================================

def appointment_details(
    appointment_id: str,
):
     return print_appointment(
        get_appointment(
            appointment_id
        )
    )


# ==========================================================
# PATIENT APPOINTMENT HISTORY
# ==========================================================

def patient_appointment_history(
    patient_id: str,
):
    bundle = get_patient_appointments(
        patient_id
    )

    appointments = []

    for entry in bundle.get(
        "entry",
        []
    ):

        resource = entry.get(
            "resource",
            {}
        )

        appointments.append(
            _format_appointment(
                resource
            )
        )

    return appointments


# ==========================================================
# PRACTITIONER SCHEDULE
# ==========================================================

def practitioner_appointment_schedule(
    practitioner_id: str,
):
    bundle = get_practitioner_appointments(
        practitioner_id
    )

    appointments = []

    for entry in bundle.get(
        "entry",
        []
    ):

        resource = entry.get(
            "resource",
            {}
        )

        appointments.append(
            _format_appointment(
                resource
            )
        )

    return appointments


# ==========================================================
# APPOINTMENTS BY DATE
# ==========================================================

def appointments_on_date(
    date: str,
):
    """
    date format:
    YYYY-MM-DD
    """

    try:
        datetime.strptime(
            date,
            "%Y-%m-%d"
        )

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date must be in YYYY-MM-DD format.",
        )

    bundle = get_appointments_by_date(
        date
    )

    appointments = []

    for entry in bundle.get(
        "entry",
        []
    ):

        resource = entry.get(
            "resource",
            {}
        )

        appointments.append(
            _format_appointment(
                resource
            )
        )

    return appointments


# ==========================================================
# RESCHEDULE APPOINTMENT
# ==========================================================

def reschedule_appointment(
    appointment_id: str,
    new_start: str,
    new_end: str,
):
    """
    Reschedule an existing appointment.

    Important:
    The existing appointment itself must not be
    treated as a conflict.
    """

    _validate_time_range(
        new_start,
        new_end,
    )

    appointment = get_appointment(
        appointment_id
    )

    current_status = appointment.get(
        "status"
    )

    if current_status in {
        "cancelled",
        "fulfilled",
        "noshow",
        "entered-in-error",
    }:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Appointment with status "
                f"'{current_status}' cannot be rescheduled."
            ),
        )

    practitioner_id = (
        get_practitioner_id_from_appointment(
            appointment
        )
    )

    patient_id = (
        get_patient_id_from_appointment(
            appointment
        )
    )

    if not practitioner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment has no practitioner.",
        )

    if not patient_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment has no patient.",
        )

    # ------------------------------------------------------
    # Practitioner conflicts
    # ------------------------------------------------------

    practitioner_conflicts = (
        get_practitioner_appointments_between(
            practitioner_id=practitioner_id,
            start=new_start,
            end=new_end,
        )
    )

    practitioner_conflicts = [
        item
        for item in practitioner_conflicts
        if item.get("id") != appointment_id
    ]

    if practitioner_conflicts:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Practitioner is not available "
                "during the requested time."
            ),
        )

    # ------------------------------------------------------
    # Patient conflicts
    # ------------------------------------------------------

    patient_conflicts = (
        get_patient_appointments_between(
            patient_id=patient_id,
            start=new_start,
            end=new_end,
        )
    )

    patient_conflicts = [
        item
        for item in patient_conflicts
        if item.get("id") != appointment_id
    ]

    if patient_conflicts:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Patient already has another appointment "
                "during the requested time."
            ),
        )

    # ------------------------------------------------------
    # Update FHIR resource
    # ------------------------------------------------------

    updated = update_appointment(
        appointment_id=appointment_id,
        start=new_start,
        end=new_end,
    )

    return {
        "success": True,
        "message": "Appointment rescheduled successfully.",
        "appointment": updated,
    }


# ==========================================================
# CANCEL
# ==========================================================

def cancel_patient_appointment(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    current_status = appointment.get(
        "status"
    )

    if current_status in {
        "cancelled",
        "fulfilled",
        "noshow",
        "entered-in-error",
    }:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Appointment with status "
                f"'{current_status}' cannot be cancelled."
            ),
        )

    cancelled = cancel_appointment(
        appointment_id
    )

    return {
        "success": True,
        "message": "Appointment cancelled.",
        "appointment": cancelled,
    }


# ==========================================================
# CHECK-IN
# ==========================================================

def check_in_patient(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    current_status = appointment.get(
        "status"
    )

    if current_status != "booked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only a booked appointment "
                "can be checked in."
            ),
        )

    updated = checkin_appointment(
        appointment_id
    )

    return {
        "success": True,
        "message": "Patient checked in successfully.",
        "appointment": updated,
    }


# ==========================================================
# COMPLETE APPOINTMENT
# ==========================================================

def complete_patient_appointment(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    current_status = appointment.get(
        "status"
    )

    if current_status != "arrived":

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Appointment must be in arrived status "
                "before completion."
            ),
        )

    updated = complete_appointment(
        appointment_id
    )

    return {
        "success": True,
        "message": "Appointment completed.",
        "appointment": updated,
    }


# ==========================================================
# MARK NO-SHOW
# ==========================================================

def mark_appointment_no_show(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    current_status = appointment.get(
        "status"
    )

    if current_status != "booked":

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only a booked appointment "
                "can be marked as no-show."
            ),
        )

    updated = mark_no_show(
        appointment_id
    )

    return {
        "success": True,
        "message": "Appointment marked as no-show.",
        "appointment": updated,
    }


# ==========================================================
# FORMAT APPOINTMENT
# ==========================================================

def _format_appointment(
    resource: dict,
):
    return {
        "id": resource.get("id"),

        "status": resource.get(
            "status"
        ),

        "patient_id": (
            get_patient_id_from_appointment(
                resource
            )
        ),

        "practitioner_id": (
            get_practitioner_id_from_appointment(
                resource
            )
        ),

        "start": resource.get(
            "start"
        ),

        "end": resource.get(
            "end"
        ),

        "reason": (
            resource.get(
                "reasonCode",
                [{}]
            )[0].get("text")
            if resource.get("reasonCode")
            else None
        ),

        "appointment_type": (
            resource.get(
                "appointmentType",
                {}
            )
            .get("coding", [{}])[0]
            .get("code")
            if resource.get("appointmentType")
            else None
        ),
    }