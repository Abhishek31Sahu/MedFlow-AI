"""
Bed Allocation API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from services.allocation_service import AllocationService

from schemas.bed_allocation import (
    BedAllocationCreate,
    BedAllocationUpdate,
    BedAllocationResponse
)

router = APIRouter(

    prefix="/allocations",

    tags=["Bed Allocation"]

)

# ==========================================================
# Create Allocation
# ==========================================================

@router.post(
    "/",
    response_model=BedAllocationResponse
)
def create_allocation(

    request: BedAllocationCreate,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.create_allocation(request)


# ==========================================================
# Get Allocation
# ==========================================================

@router.get(
    "/{allocation_id}",
    response_model=BedAllocationResponse
)
def get_allocation(

    allocation_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.get_allocation(
        allocation_id
    )


# ==========================================================
# Get Active Allocation
# ==========================================================

@router.get(
    "/patient/{patient_id}/active",
    response_model=BedAllocationResponse
)
def get_active_allocation(

    patient_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.get_active_allocation(
        patient_id
    )


# ==========================================================
# Patient History
# ==========================================================

@router.get(
    "/patient/{patient_id}/history"
)
def patient_history(

    patient_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.get_patient_history(
        patient_id
    )


# ==========================================================
# Bed History
# ==========================================================

@router.get(
    "/bed/{bed_id}/history"
)
def bed_history(

    bed_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.get_bed_history(
        bed_id
    )


# ==========================================================
# Complete Allocation
# ==========================================================

@router.put(
    "/{allocation_id}/complete",
    response_model=BedAllocationResponse
)
def complete_allocation(

    allocation_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.complete_allocation(
        allocation_id
    )


# ==========================================================
# Cancel Allocation
# ==========================================================

@router.put(
    "/{allocation_id}/cancel",
    response_model=BedAllocationResponse
)
def cancel_allocation(

    allocation_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return service.cancel_allocation(
        allocation_id
    )


# ==========================================================
# Delete Allocation
# ==========================================================

@router.delete(
    "/{allocation_id}"
)
def delete_allocation(

    allocation_id: str,

    db: Session = Depends(get_db)

):

    service = AllocationService(db)

    return {

        "success": service.delete_allocation(
            allocation_id
        )

    }