"""
Bed Management API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import require_roles
from database.database import get_db
from models.enums import UserRole
from models.user import User

from schemas.bed import (
    BedCreate,
    BedUpdate,
    BedResponse,
)

from schemas.bed_recommendation import (
    BedRecommendationRequest,
    BedRecommendationResponse,
    BedAssignmentRequest,
    BedTransferRequest,
)

from services.bed_service import (
    BedService,
    BedRecommendationService,
)


router = APIRouter(
    prefix="/beds",
    tags=["Bed Management"],
)


# ============================================================
# CRUD
# ============================================================

# ------------------------------------------------------------
# CREATE BED
# Admin only
# ------------------------------------------------------------

@router.post(
    "",
    response_model=BedResponse,
)
def create_bed(
    request: BedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    return BedService(db).create_bed(request)


# ------------------------------------------------------------
# GET ALL BEDS
# Admin, Doctor, Nurse, Receptionist
# ------------------------------------------------------------

@router.get(
    "",
    response_model=list[BedResponse],
)
def get_all_beds(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return BedService(db).get_all_beds()


# ------------------------------------------------------------
# GET SINGLE BED
# Admin, Doctor, Nurse, Receptionist
# ------------------------------------------------------------

@router.get(
    "/{bed_id}",
    response_model=BedResponse,
)
def get_bed(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return BedService(db).get_bed(bed_id)


# ------------------------------------------------------------
# UPDATE BED
# Admin only
# ------------------------------------------------------------

@router.put(
    "/{bed_id}",
    response_model=BedResponse,
)
def update_bed(
    bed_id: str,
    request: BedUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    return BedService(db).update_bed(
        bed_id,
        request,
    )


# ------------------------------------------------------------
# DELETE BED
# Admin only
# ------------------------------------------------------------

@router.delete(
    "/{bed_id}",
)
def delete_bed(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    return BedService(db).delete_bed(bed_id)


# ============================================================
# AI RECOMMENDATION
# ============================================================

@router.post(
    "/recommend",
    response_model=list[BedRecommendationResponse],
)
def recommend_beds(
    request: BedRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedRecommendationService(db).recommend_beds(
        request
    )


# ============================================================
# ASSIGNMENT
# ============================================================

@router.post(
    "/assign",
)
def assign_bed(
    request: BedAssignmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).assign_bed(
        request
    )


# ============================================================
# RELEASE
# ============================================================

@router.post(
    "/{bed_id}/release",
)
def release_bed(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).release_bed(
        bed_id
    )


# ============================================================
# RESERVATION
# ============================================================

@router.post(
    "/{bed_id}/reserve",
)
def reserve_bed(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).reserve_bed(
        bed_id
    )


@router.post(
    "/{bed_id}/cancel-reservation",
)
def cancel_reservation(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).release_reserved_bed(
        bed_id
    )


# ============================================================
# TRANSFER
# ============================================================

@router.post(
    "/transfer",
)
def transfer_bed(
    request: BedTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    service = BedService(db)

    service.release_bed_by_encounter_id(
        request.encounter_id
    )

    return service.assign_bed(
        BedAssignmentRequest(
            bed_id=request.new_bed_id,
            patient_id=request.patient_id,
            encounter_id=request.encounter_id,
        )
    )


# ============================================================
# CLEANING
# ============================================================

@router.post(
    "/{bed_id}/cleaning",
)
def mark_cleaning(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).mark_cleaning(
        bed_id
    )


# ============================================================
# AVAILABLE
# ============================================================

@router.post(
    "/{bed_id}/available",
)
def mark_available(
    bed_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).mark_available(
        bed_id
    )


# ============================================================
# DASHBOARD
# ============================================================

# ------------------------------------------------------------
# BED STATISTICS
# Admin, Doctor, Nurse
# ------------------------------------------------------------

@router.get(
    "/dashboard/statistics",
)
def dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
        )
    ),
):
    return BedService(db).get_bed_statistics()


# ------------------------------------------------------------
# AVAILABLE BEDS
# Admin, Doctor, Nurse, Receptionist
# ------------------------------------------------------------

@router.get(
    "/dashboard/available",
)
def available_beds(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return BedService(db).get_available_beds()


# ------------------------------------------------------------
# OCCUPIED BEDS
# Admin, Doctor, Nurse, Receptionist
# ------------------------------------------------------------

@router.get(
    "/dashboard/occupied",
)
def occupied_beds(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.RECEPTIONIST,
        )
    ),
):
    return BedService(db).get_occupied_beds()