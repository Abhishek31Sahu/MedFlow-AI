"""
Practitioner Schedule Service

Business logic for practitioner working schedules.
"""

from datetime import date, time

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.practitioner_schedule import PractitionerSchedule


VALID_DAYS = {
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
}


# ==========================================================
# VALIDATION
# ==========================================================

def _validate_day(
    day_of_week: str,
) -> str:

    day = day_of_week.strip().lower()

    if day not in VALID_DAYS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid day_of_week. "
                "Use monday through sunday."
            ),
        )

    return day


def _validate_time_range(
    start_time: time,
    end_time: time,
):

    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time.",
        )


# ==========================================================
# CREATE SCHEDULE
# ==========================================================

def create_schedule(
    db: Session,
    practitioner_id: str,
    day_of_week: str,
    start_time: time,
    end_time: time,
):
    day = _validate_day(
        day_of_week
    )

    _validate_time_range(
        start_time,
        end_time,
    )

    # ------------------------------------------------------
    # Check exact duplicate
    # ------------------------------------------------------

    existing = (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.practitioner_id
            == practitioner_id,
            PractitionerSchedule.day_of_week
            == day,
            PractitionerSchedule.start_time
            == start_time,
            PractitionerSchedule.end_time
            == end_time,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This schedule already exists "
                "for the practitioner."
            ),
        )

    # ------------------------------------------------------
    # Check overlapping schedule
    # ------------------------------------------------------

    overlapping = (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.practitioner_id
            == practitioner_id,
            PractitionerSchedule.day_of_week
            == day,
            PractitionerSchedule.is_active
            == True,
        )
        .all()
    )

    for item in overlapping:

        if (
            start_time < item.end_time
            and end_time > item.start_time
        ):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "The new schedule overlaps "
                    "with an existing schedule."
                ),
            )

    # ------------------------------------------------------
    # Create
    # ------------------------------------------------------

    schedule = PractitionerSchedule(
        practitioner_id=practitioner_id,
        day_of_week=day,
        start_time=start_time,
        end_time=end_time,
        is_active=True,
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


# ==========================================================
# GET PRACTITIONER SCHEDULE
# ==========================================================

def get_practitioner_schedule(
    db: Session,
    practitioner_id: str,
):

    return (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.practitioner_id
            == practitioner_id,
            PractitionerSchedule.is_active
            == True,
        )
        .order_by(
            PractitionerSchedule.day_of_week,
            PractitionerSchedule.start_time,
        )
        .all()
    )


# ==========================================================
# GET SCHEDULE FOR A PARTICULAR DAY
# ==========================================================

def get_schedule_for_day(
    db: Session,
    practitioner_id: str,
    day_of_week: str,
):

    day = _validate_day(
        day_of_week
    )

    return (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.practitioner_id
            == practitioner_id,
            PractitionerSchedule.day_of_week
            == day,
            PractitionerSchedule.is_active
            == True,
        )
        .order_by(
            PractitionerSchedule.start_time
        )
        .all()
    )


# ==========================================================
# GET TODAY'S SCHEDULE
# ==========================================================

def get_today_schedule(
    db: Session,
    practitioner_id: str,
):

    today = date.today()

    day_name = today.strftime(
        "%A"
    ).lower()

    return get_schedule_for_day(
        db=db,
        practitioner_id=practitioner_id,
        day_of_week=day_name,
    )


# ==========================================================
# IS PRACTITIONER WORKING TODAY?
# ==========================================================

def is_practitioner_working_today(
    db: Session,
    practitioner_id: str,
):

    schedules = get_today_schedule(
        db=db,
        practitioner_id=practitioner_id,
    )

    return {
        "working_today": len(schedules) > 0,
        "day": date.today().strftime("%A").lower(),
        "schedule": schedules,
    }


# ==========================================================
# UPDATE SCHEDULE
# ==========================================================

def update_schedule(
    db: Session,
    schedule_id: str,
    start_time: time | None = None,
    end_time: time | None = None,
    is_active: bool | None = None,
):

    schedule = (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.id
            == schedule_id
        )
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found.",
        )

    new_start = (
        start_time
        if start_time is not None
        else schedule.start_time
    )

    new_end = (
        end_time
        if end_time is not None
        else schedule.end_time
    )

    _validate_time_range(
        new_start,
        new_end,
    )

    if start_time is not None:
        schedule.start_time = start_time

    if end_time is not None:
        schedule.end_time = end_time

    if is_active is not None:
        schedule.is_active = is_active

    db.commit()
    db.refresh(schedule)

    return schedule


# ==========================================================
# DELETE / DEACTIVATE SCHEDULE
# ==========================================================

def delete_schedule(
    db: Session,
    schedule_id: str,
):

    schedule = (
        db.query(PractitionerSchedule)
        .filter(
            PractitionerSchedule.id
            == schedule_id
        )
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found.",
        )

    # Soft delete
    schedule.is_active = False

    db.commit()

    return {
        "success": True,
        "message": "Schedule removed successfully.",
    }