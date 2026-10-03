from typing import Optional

from pydantic import BaseModel, Field


class LabTest(BaseModel):

    code: Optional[str] = Field(
        default=None,
        description="LOINC code if available."
    )

    name: str = Field(
        description="Laboratory test name."
    )


class ExtractedLabOrder(BaseModel):

    patient_name: str

    tests: list[LabTest]

    priority: str = "routine"

    clinical_note: Optional[str] = None