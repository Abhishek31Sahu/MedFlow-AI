from pydantic import BaseModel


class ObservationDecision(BaseModel):

    function: str

    payload: dict