from fastapi import APIRouter, Depends

from core.security import require_roles
from models.enums import UserRole
from models.user import User

from patient.patient import (
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


# ==========================================================
# CREATE PATIENT
# Admin, Doctor, Receptionist
# ==========================================================

@router.post("/")
def add_patient(
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return create_patient(
        first_name=data["first_name"],
        last_name=data["last_name"],
        gender=data["gender"],
        birth_date=data["birth_date"],
    )


# ==========================================================
# GET ALL PATIENTS
# Admin, Doctor, Nurse, Receptionist,
# Lab Technician, Pharmacist
# ==========================================================

@router.get("/all")
def get_all_patients(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
            UserRole.LAB_TECHNICIAN,
            UserRole.PHARMACIST,
        )
    ),
):
    return fetch_all_patients()


# ==========================================================
# GET SINGLE PATIENT
# All authenticated hospital roles
# ==========================================================

@router.get("/{patient_id}")
def read_patient(
    patient_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
            UserRole.LAB_TECHNICIAN,
            UserRole.PHARMACIST,
        )
    ),
):
    return get_patient(patient_id)


# ==========================================================
# UPDATE PATIENT
# Admin, Doctor, Receptionist
# ==========================================================

@router.put("/{patient_id}")
def edit_patient(
    patient_id: str,
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return update_patient(
        patient_id=patient_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        gender=data.get("gender"),
        birth_date=data.get("birth_date"),
    )


# ==========================================================
# DELETE PATIENT
# Admin only
# ==========================================================

@router.delete("/{patient_id}")
def remove_patient(
    patient_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    return delete_patient(patient_id)