"""
Laboratory API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from core.security import require_roles

from models.enums import UserRole
from models.user import User

from services.laboratory_service import LaboratoryService

from schemas.laboratory import (
    CreateLabOrderRequest,
    SubmitLabResultRequest,
)


router = APIRouter(
    prefix="/laboratory",
    tags=["Laboratory"],
)


# ==========================================================
# CREATE LAB ORDER
# Doctor + Admin
# ==========================================================

@router.post("/orders")
async def create_lab_order(
    request: CreateLabOrderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
        )
    ),
):
    service = LaboratoryService(db)

    return service.create_lab_order(request)


# ==========================================================
# PENDING LAB ORDERS
# Admin + Doctor + Lab Technician
# ==========================================================

@router.get("/orders/pending")
async def get_pending_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_pending_orders()


# ==========================================================
# PATIENT ORDERS
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get("/orders/patient/{patient_id}")
async def get_patient_orders(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_patient_orders(
        patient_id
    )


# ==========================================================
# ORDER BY SERVICE REQUEST
# Admin + Doctor + Lab Technician
# ==========================================================

@router.get(
    "/orders/service_request/{service_request_id}"
)
async def get_laboratory_orders(
    service_request_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_laboratory_orders(
        service_request_id
    )


# ==========================================================
# SUBMIT LAB RESULTS
# Lab Technician + Admin
# ==========================================================

@router.post("/results")
async def submit_results(
    report: SubmitLabResultRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.submit_results(
        report
    )


# ==========================================================
# DIAGNOSTIC REPORT BY REPORT ID
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get("/reports/{report_id}")
async def get_reports(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_report(
        report_id
    )


# ==========================================================
# DIAGNOSTIC REPORTS BY PATIENT
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get(
    "/reports/patient/{patient_id}"
)
async def get_report_by_patient_id(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_report_by_patient_id(
        patient_id
    )


# ==========================================================
# REPORT BY SERVICE REQUEST
# Admin + Doctor + Nurse + Lab Technician
# ==========================================================

@router.get(
    "/reports/service_request/{service_request_id}"
)
async def get_report(
    service_request_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.NURSE,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_report_by_service_request(
        service_request_id
    )


# ==========================================================
# PENDING FHIR ORDERS
# Lab Technician + Admin
# ==========================================================

@router.get("/fhir/pending")
async def get_pending_fhir_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):
    service = LaboratoryService(db)

    return service.get_pending_fhir_orders()