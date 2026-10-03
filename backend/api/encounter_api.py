"""
Encounter API
"""

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import require_roles

from models.enums import UserRole
from models.user import User

from services.encounter_service import (
    admit_patient,
    encounter_details,
    patient_encounter_history,
    transfer_to_new_location,
    discharge_patient,
    cancel_patient_encounter,
    all_encounters
)


router = APIRouter(
    prefix="/encounters",
    tags=["Encounter"],
)


# ==========================================================
# CREATE ENCOUNTER (Admission)
# Admin + Doctor
# ==========================================================
@router.get("/")
def get_all_encounters_endpoint(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return all_encounters()

@router.post("/")
def create_encounter(
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    # ------------------------------------------------------
    # Doctor -> use logged-in doctor's Practitioner ID
    # ------------------------------------------------------

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "No FHIR Practitioner ID is linked "
                    "to this doctor account."
                ),
            )

        practitioner_id = current_user.practitioner_id

    # ------------------------------------------------------
    # Admin -> practitioner ID may be provided
    # ------------------------------------------------------

    else:

        practitioner_id = data.get(
            "practitioner_id"
        )

        if not practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="practitioner_id is required.",
            )

    return admit_patient(

        patient_id=data["patient_id"],

        practitioner_id=practitioner_id,

        location_id=data["location_id"],

        encounter_type=data.get(
            "encounter_type",
            "IMP",
        ),

        service_type=data.get(
            "service_type",
            "General Medicine",
        ),

        reason=data.get(
            "reason",
            "General Checkup",
        ),

        priority=data.get(
            "priority",
            "routine",
        ),

        diagnosis=data.get(
            "diagnosis"
        ),

        admission_source=data.get(
            "admission_source"
        ),
    )


# ==========================================================
# GET PATIENT ENCOUNTERS
# IMPORTANT:
# Keep static route before /{encounter_id}
# ==========================================================

@router.get("/patient/{patient_id}")
def get_patient_history(
    patient_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):

    return patient_encounter_history(
        patient_id
    )


# ==========================================================
# GET ENCOUNTER
# Admin + Doctor + Nurse + Receptionist
# ==========================================================

@router.get("/{encounter_id}")
def get_encounter(
    encounter_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):

    return encounter_details(
        encounter_id
    )


# ==========================================================
# TRANSFER PATIENT
# Admin + Doctor + Nurse
# ==========================================================

@router.put("/{encounter_id}/transfer")
def transfer(
    encounter_id: str,
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):

    return transfer_to_new_location(

        encounter_id,

        data["location_id"]

    )


# ==========================================================
# DISCHARGE PATIENT
# Admin + Doctor
# ==========================================================

@router.put("/{encounter_id}/complete")
def complete(
    encounter_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    return discharge_patient(
        encounter_id
    )


# ==========================================================
# CANCEL ENCOUNTER
# Admin + Doctor
# ==========================================================

@router.put("/{encounter_id}/cancel")
def cancel(
    encounter_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    return cancel_patient_encounter(
        encounter_id
    )