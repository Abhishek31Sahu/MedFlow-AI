from fastapi import APIRouter, Depends, HTTPException, status

from core.security import require_roles
from models.enums import UserRole
from models.user import User

from services.admission_service import admit_patient


router = APIRouter(
    prefix="/admission",
    tags=["Admission"],
)


# ==========================================================
# ADMIT PATIENT
# Admin + Doctor
# ==========================================================

@router.post("/")
def admit(
    data: dict,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):

    # ------------------------------------------------------
    # Doctor: use logged-in doctor's Practitioner ID
    # instead of trusting practitioner_id from frontend.
    # ------------------------------------------------------

    if current_user.role == UserRole.DOCTOR:

        if not current_user.practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No FHIR Practitioner ID linked to this doctor account.",
            )

        practitioner_id = current_user.practitioner_id

    # ------------------------------------------------------
    # Admin can provide Practitioner ID explicitly
    # ------------------------------------------------------

    else:
        practitioner_id = data.get("practitioner_id")

        if not practitioner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="practitioner_id is required for admin admission.",
            )

    return admit_patient(
        patient_id=data["patient_id"],
        practitioner_id=practitioner_id,
        ward=data["ward"],
    )