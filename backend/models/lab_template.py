from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from database.database import Base
import uuid

class LabTemplate(Base):
    __tablename__ = "lab_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    test_code = Column(String, unique=True, nullable=False)   # CBC
    test_name = Column(String, nullable=False)                # Complete Blood Count
    category = Column(String, nullable=True)                  # Hematology
    description = Column(Text, nullable=True)

    parameters = relationship(
        "LabParameter",
        back_populates="template",
        cascade="all, delete-orphan",
        order_by="LabParameter.display_order",
    )