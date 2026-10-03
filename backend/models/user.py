from sqlalchemy import Column, String, Boolean, DateTime
from database.database import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    # Internal application user ID
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Login information
    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    # Hospital employee information
    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    department = Column(
        String,
        nullable=True
    )

    designation = Column(
        String,
        nullable=True
    )

    # FHIR Practitioner ID
    # Example: "1053"
    practitioner_id = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )

    # Hospital role
    # admin / doctor / nurse / lab_technician / receptionist / pharmacist
    role = Column(
        String,
        nullable=False,
        default="staff",
        index=True
    )

    # Account status
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # Audit information
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )