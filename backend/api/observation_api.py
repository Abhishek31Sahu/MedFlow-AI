"""
Observation API
"""

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import require_roles

from models.enums import UserRole
from models.user import User

from services.observation_service import (
    add_observation,
    get_observation_details,
    list_patient_observations,
    search_test,
    latest_test_result,
    change_observation_value,
    remove_observation,
)


router = APIRouter(
    prefix="/observations",
    tags=["Observation"],
)


# ==========================================================
# CREATE OBSERVATION
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.post("/")
def create_observation(
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    # ------------------------------------------------------
    # Doctor -> use logged-in doctor's FHIR Practitioner ID
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

    else:
        # Admin / Nurse / Lab Technician
        practitioner_id = data.get("practitioner_id")

        if not practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="practitioner_id is required.",
            )

    return add_observation(

        patient_id=data["patient_id"],

        practitioner_id=practitioner_id,

        encounter_id=data["encounter_id"],

        code=data["test_code"],
        display=data["test_name"],

        value=data["value"],

        unit=data["unit"],

        category=data.get(
            "category",
            "laboratory"
        ),

        interpretation=data.get(
            "interpretation"
        ),

        note=data.get(
            "note"
        ),

        low_reference=data.get(
            "low_reference"
        ),

        high_reference=data.get(
            "high_reference"
        ),
    )


# ==========================================================
# GET OBSERVATION
# Admin + Doctor + Nurse + Lab Technician + Pharmacist
# ==========================================================

@router.get("/{observation_id}")
def get_observation(
    observation_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
            UserRole.PHARMACIST,
        )
    ),
):

    return get_observation_details(
        observation_id
    )


# ==========================================================
# GET PATIENT OBSERVATIONS
# Admin + Doctor + Nurse + Lab Technician + Pharmacist
# ==========================================================

@router.get("/patient/{patient_id}")
def get_patient_observations(
    patient_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
            UserRole.PHARMACIST,
        )
    ),
):

    return list_patient_observations(
        patient_id
    )


# ==========================================================
# SEARCH TEST
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get(
    "/patient/{patient_id}/test/{test_name}"
)
def get_test(
    patient_id: str,
    test_name: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    return search_test(
        patient_id,
        test_name
    )


# ==========================================================
# LATEST TEST RESULT
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get(
    "/patient/{patient_id}/latest/{test_name}"
)
def latest_result(
    patient_id: str,
    test_name: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    return latest_test_result(
        patient_id,
        test_name
    )


# ==========================================================
# UPDATE OBSERVATION
# Admin + Doctor + Lab Technician
# ==========================================================

@router.put("/{observation_id}")
def update_value(
    observation_id: str,
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    return change_observation_value(
        observation_id,
        data["value"]
    )


# ==========================================================
# DELETE OBSERVATION
# Admin only
# ==========================================================

@router.delete("/{observation_id}")
def delete_observation(
    observation_id: str,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN
        )
    ),
):

    return remove_observation(
        observation_id
    )