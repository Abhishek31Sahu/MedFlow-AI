"""
Medication API

REST endpoints for medication management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.medication_service import (
    add_medication,
    discontinue_medication,
    change_dosage,
    list_active_medications,
    medication_history,
    get_all_active_medications
)

router = APIRouter(
    prefix="/medications",
    tags=["Medications"],
)


# ==========================================================
# REQUEST SCHEMAS
# ==========================================================

class AddMedicationRequest(BaseModel):
    patient_id: str
    practitioner_id: str
    medicine_name: str
    dosage: str
    frequency: str


class StopMedicationRequest(BaseModel):
    patient_id: str
    medicine_name: str


class ChangeDosageRequest(BaseModel):
    patient_id: str
    medicine_name: str
    dosage: str
    frequency: str


# ==========================================================
# ADD MEDICATION
# ==========================================================

@router.post("/")
def create_medication(request: AddMedicationRequest):

    return add_medication(
        patient_id=request.patient_id,
        practitioner_id=request.practitioner_id,
        medicine_name=request.medicine_name,
        dosage=request.dosage,
        frequency=request.frequency,
    )


# ==========================================================
# STOP MEDICATION
# ==========================================================

@router.put("/stop")
def stop_medication(request: StopMedicationRequest):

    return discontinue_medication(
        patient_id=request.patient_id,
        medicine_name=request.medicine_name,
    )


# ==========================================================
# CHANGE DOSAGE
# ==========================================================

@router.put("/dosage")
def update_medication_dosage(
    request: ChangeDosageRequest,
):

    return change_dosage(
        patient_id=request.patient_id,
        medicine_name=request.medicine_name,
        dosage=request.dosage,
        frequency=request.frequency,
    )


# ==========================================================
# ACTIVE MEDICATIONS
# ==========================================================

@router.get("/patient/{patient_id}/active")
def get_active_medications(
    patient_id: str,
):

    return list_active_medications(patient_id)


# ==========================================================
# MEDICATION HISTORY
# ==========================================================

@router.get("/patient/{patient_id}/history")
def get_medication_history(
    patient_id: str,
):

    return medication_history(patient_id)


@router.get("/all")
def get_all_medications():
    return get_all_active_medications()