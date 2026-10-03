from pydantic import BaseModel


class SummaryDecision(BaseModel):

    function: str

    payload: dict