from typing import List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# Lab Parameter
# ==========================================================

class LabParameterBase(BaseModel):
    code: str = Field(..., example="718-7")
    name: str = Field(..., example="Hemoglobin")
    unit: Optional[str] = Field(None, example="g/dL")

    value_type: str = Field(
        default="number",
        example="number",
        description="number | text | boolean | choice",
    )

    reference_low: Optional[float] = None
    reference_high: Optional[float] = None

    required: bool = True


class LabParameterCreate(LabParameterBase):
    pass


class LabParameterResponse(LabParameterBase):
    id: str
    display_order: int

    class Config:
        from_attributes = True


# ==========================================================
# Create Template
# ==========================================================

class CreateTemplateRequest(BaseModel):
    test_code: str = Field(..., example="CBC")

    test_name: str = Field(
        ...,
        example="Complete Blood Count",
    )

    category: Optional[str] = Field(
        None,
        example="Hematology",
    )

    description: Optional[str] = None

    parameters: List[LabParameterCreate]


# ==========================================================
# Update Template
# ==========================================================

class UpdateTemplateRequest(BaseModel):
    test_name: str

    category: Optional[str] = None

    description: Optional[str] = None

    parameters: List[LabParameterCreate]


# ==========================================================
# Response
# ==========================================================

class LabTemplateResponse(BaseModel):
    id: str

    test_code: str

    test_name: str

    category: Optional[str]

    description: Optional[str]

    parameters: List[LabParameterResponse]

    class Config:
        from_attributes = True