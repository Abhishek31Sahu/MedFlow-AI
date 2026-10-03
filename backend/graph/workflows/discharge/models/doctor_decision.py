from typing import Literal

from pydantic import BaseModel


class DoctorDecision(BaseModel):

    medication_id: str

    medicine_name: str

    final_action: Literal[
        "continue",
        "stop",
        "modify"
    ]

    accepted_ai_recommendation: bool = True

    dosage: str | None = None

    frequency: str | None = None

    override_reason: str | None = None