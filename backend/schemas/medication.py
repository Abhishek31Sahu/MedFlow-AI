from pydantic import BaseModel


class MedicationInfo(BaseModel):
    id: str
    medicine: str
    status: str
    dosage: str
    
class AddMedicationRequest(BaseModel):
    patient_id: str
    practitioner_id: str
    medicine_name: str
    dosage: str
    frequency: str


class MedicationResponse(BaseModel):
    success: bool
    message: str
    medication_request_id: str | None = None