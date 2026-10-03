from typing import Optional

from pydantic import BaseModel


class PatientSearchInput(BaseModel):

    name: str


class PatientSearchResult(BaseModel):

    patient_id: str

    name: str

    gender: Optional[str] = None

    birth_date: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None