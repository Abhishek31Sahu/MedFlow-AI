"""
Discharge Workflow Input Model
"""

from pydantic import BaseModel, Field


class DischargeInput(BaseModel):
    """
    Information extracted from the user's discharge request.
    """

    # Required
    patient_name: str = Field(
        description="Name of the patient to discharge."
    )

    # Optional
    reason: str | None = Field(
        default=None,
        description="Reason for discharge if mentioned."
    )

    discharge_date: str | None = Field(
        default=None,
        description="Requested discharge date or time."
    )

    follow_up: str | None = Field(
        default=None,
        description="Follow-up instructions if mentioned."
    )