import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String
)

from sqlalchemy.sql import func

from database.database import Base

from models.enums import (
    BedStatus,
    BedType,
    GenderPolicy
)


class Bed(Base):

    __tablename__ = "beds"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    bed_number = Column(
        String,
        unique=True,
        nullable=False
    )

    ward = Column(
        String,
        nullable=False
    )

    room_number = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        nullable=False
    )

    floor = Column(
        String,
        nullable=True
    )

    location_id = Column(
        String,
        nullable=False
    )

    bed_type = Column(
        String,
        default=BedType.GENERAL.value,
        nullable=False
    )

    status = Column(
        String,
        default=BedStatus.AVAILABLE.value,
        nullable=False
    )

    gender_policy = Column(
        String,
        default=GenderPolicy.ANY.value
    )

    oxygen = Column(
        Boolean,
        default=False
    )

    ventilator = Column(
        Boolean,
        default=False
    )

    isolation = Column(
        Boolean,
        default=False
    )

    cardiac_monitor = Column(
        Boolean,
        default=False
    )

    dialysis = Column(
        Boolean,
        default=False
    )

    pediatric = Column(
        Boolean,
        default=False
    )

    maternity = Column(
        Boolean,
        default=False
    )

    cleaning_required = Column(
        Boolean,
        default=False
    )

    occupied_by = Column(
        String,
        nullable=True
    )

    encounter_id = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )