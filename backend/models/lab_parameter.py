from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from database.database import Base
import uuid

class LabParameter(Base):
    __tablename__ = "lab_parameters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    template_id = Column(
        String,
        ForeignKey("lab_templates.id", ondelete="CASCADE"),
        nullable=False,
    )

    code = Column(String, nullable=False)          # LOINC Code
    name = Column(String, nullable=False)          # Hemoglobin

    unit = Column(String, nullable=True)           # g/dL

    value_type = Column(
        String,
        nullable=False,
        default="number",
    )
    # number
    # text
    # boolean
    # choice

    reference_low = Column(Float, nullable=True)
    reference_high = Column(Float, nullable=True)

    required = Column(Boolean, default=True)

    display_order = Column(Integer, default=1)

    template = relationship(
        "LabTemplate",
        back_populates="parameters",
    )