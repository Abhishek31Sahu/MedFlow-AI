"""
Transfer Workflow Input
"""

from pydantic import BaseModel


class TransferInput(BaseModel):

    # Name mentioned by the doctor
    patient_name: str

    # Destination location
    destination_location: str

    # Optional transfer reason
    reason: str | None = None