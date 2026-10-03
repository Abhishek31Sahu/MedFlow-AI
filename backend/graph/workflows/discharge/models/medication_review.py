"""
AI Medication Review Models
"""

from typing import Literal

from pydantic import BaseModel, Field


# ==========================================================
# Recommendation for One Medication
# ==========================================================

class MedicationRecommendation(BaseModel):

    medicine_name: str = Field(
        description="Medicine name."
    )

    recommendation: Literal[
        "continue",
        "consider_stop",
        "consider_modify"
    ]

    reason: str = Field(
        description="Why the recommendation was made."
    )


# ==========================================================
# Overall AI Review
# ==========================================================

class MedicationReview(BaseModel):

    recommendations: list[
        MedicationRecommendation
    ]

    summary: str

    requires_doctor_approval: bool = True