
from pydantic import BaseModel

class AdmissionInput(BaseModel):

    patient_name: str

    department: str | None = None
    
    reason_for_admission: str
    


