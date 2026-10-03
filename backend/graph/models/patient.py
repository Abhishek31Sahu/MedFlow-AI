from pydantic import BaseModel


class PatientDecision(BaseModel):

    function: str

    payload: dict