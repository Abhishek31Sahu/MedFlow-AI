"""
Practitioner Schedule Model

Stores the recurring working schedule of a practitioner.
"""

from datetime import datetime, time
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
    Time,
    UniqueConstraint,
)

from database.database import Base


class PractitionerSchedule(Base):

    __tablename__ = "practitioner_schedules"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    # FHIR Practitioner/{id}
    practitioner_id = Column(
        String,
        nullable=False,
        index=True,
    )

    # 0 = Monday ... 6 = Sunday
    day_of_week = Column(
        String,
        nullable=False,
        index=True,
    )

    start_time = Column(
        Time,
        nullable=False,
    )

    end_time = Column(
        Time,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "practitioner_id",
            "day_of_week",
            "start_time",
            "end_time",
            name="uq_practitioner_schedule",
        ),
    )