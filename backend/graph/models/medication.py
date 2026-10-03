from pydantic import BaseModel


class MedicationDecision(BaseModel):

    function: str

    payload: dict