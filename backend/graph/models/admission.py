from pydantic import BaseModel


class AdmissionInput(BaseModel):

    patient_id: str

    location_name: str

    encounter_type: str = "IMP"