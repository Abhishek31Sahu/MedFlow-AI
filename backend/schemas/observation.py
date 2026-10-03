from pydantic import BaseModel


class ObservationInfo(BaseModel):
    test: str
    value: float
    unit: str
    date: str