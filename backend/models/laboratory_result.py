from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database.database import Base


class LaboratoryResult(Base):
    __tablename__ = "laboratory_results"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    laboratory_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("laboratory_orders.id"),
        nullable=False,
        index=True,
    )

    diagnostic_report_id = Column(
        String,
        nullable=False,
        unique=True,
    )

    service_request_id = Column(
        String,
        nullable=False,
        index=True,
    )

    generated_by = Column(
        String,
        nullable=False,
    )

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )