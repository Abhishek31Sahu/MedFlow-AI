from fastapi import APIRouter, HTTPException

from services.practitioner_service import (
    register_practitioner,
    practitioner_details,
)

router = APIRouter(
    prefix="/practitioners",
    tags=["Practitioner"],
)


# ==========================================================
# CREATE PRACTITIONER
# ==========================================================

@router.post("/")
def create(data: dict):

    try:
        return register_practitioner(
            first_name=data["first_name"],
            last_name=data.get("last_name", ""),
            gender=data.get("gender"),
            phone=data.get("phone"),
            email=data.get("email"),
            designation=data.get("designation"),
        )

    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# GET PRACTITIONER
# ==========================================================

@router.get("/{practitioner_id}")
def get(practitioner_id: str):

    try:
        return practitioner_details(
            practitioner_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )