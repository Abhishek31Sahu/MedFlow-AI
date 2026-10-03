from pydantic import BaseModel


class PatientInfo(BaseModel):
    id: str
    name: str
    gender: str | None = None
    birth_date: str | None = None