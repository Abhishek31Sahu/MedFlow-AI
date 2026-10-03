from pydantic import BaseModel


class EncounterDecision(BaseModel):

    function: str

    payload: dict