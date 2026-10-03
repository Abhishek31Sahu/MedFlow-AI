from pydantic import BaseModel

from schemas.patient import PatientInfo
from schemas.medication import MedicationInfo
from schemas.encounter import EncounterInfo
from schemas.observation import ObservationInfo


class PatientSummary(BaseModel):
    patient: PatientInfo
    encounters: list[EncounterInfo]
    medications: list[MedicationInfo]
    observations: list[ObservationInfo]