"""
Bed Allocation Model
"""

import uuid

from datetime import datetime

from models.enums import (
    AllocationStatus,
    AllocationType
)

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey
)

from database.database import Base


import uuid

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Float,
    ForeignKey,
    Text
)

from database.database import Base


class BedAllocation(Base):

    __tablename__ = "bed_allocations"

    # ==========================================================
    # Primary Key
    # ==========================================================

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ==========================================================
    # References
    # ==========================================================

    bed_id = Column(
        String,
        ForeignKey("beds.id"),
        nullable=False
    )

    patient_id = Column(
        String,
        nullable=False
    )

    encounter_id = Column(
        String,
        nullable=False
    )

    # ==========================================================
    # Allocation Details
    # ==========================================================

    allocated_by = Column(
        String,
        nullable=True
    )

    allocation_type = Column(
        String,
        default=AllocationType.ADMISSION.value
    )
    # ADMISSION
    # TRANSFER
    # MANUAL

    # ==========================================================
    # AI Recommendation
    # ==========================================================

    recommendation_score = Column(
        Float,
        nullable=True
    )

    recommendation_reason = Column(
        Text,
        nullable=True
    )

    # Example:
    # Department Match
    # Oxygen Available
    # ICU Bed

    # ==========================================================
    # Timeline
    # ==========================================================

    allocated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    released_at = Column(
        DateTime,
        nullable=True
    )

    # ==========================================================
    # Status
    # ==========================================================

    status = Column(
        String,
        default=AllocationStatus.ACTIVE.value
    )

    # ACTIVE
    # COMPLETED
    # CANCELLED