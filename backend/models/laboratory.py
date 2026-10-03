from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.sql import func

from database.database import Base
from models.enums import (
    LabOrderStatus,
    SampleStatus,
    Priority,
)


class LaboratoryOrder(Base):
    __tablename__ = "laboratory_orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # FHIR References
    service_request_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    patient_id = Column(
        String,
        nullable=False,
        index=True,
    )

    encounter_id = Column(
        String,
        nullable=True,
    )

    practitioner_id = Column(
        String,
        nullable=False,
    )

    technician_id = Column(
        String,
        nullable=True,
    )

    test_code = Column(
        String,
        nullable=False,
    )

    test_name = Column(
        String,
        nullable=False,
    )

    priority = Column(
        SqlEnum(Priority),
        default=Priority.ROUTINE,
        nullable=False,
    )

    status = Column(
        SqlEnum(LabOrderStatus),
        default=LabOrderStatus.PENDING,
        nullable=False,
    )

    sample_status = Column(
        SqlEnum(SampleStatus),
        default=SampleStatus.NOT_COLLECTED,
        nullable=False,
    )

    clinical_note = Column(
        Text,
        nullable=True,
    )

    ordered_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )