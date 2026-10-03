"""
Laboratory Template API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db

from core.security import require_roles
from models.enums import UserRole
from models.user import User

from services.template_service import TemplateService

from schemas.lab_template import (
    CreateTemplateRequest,
    UpdateTemplateRequest,
    LabTemplateResponse,
)


router = APIRouter(
    prefix="/laboratory/templates",
    tags=["Laboratory Templates"],
)


# ==========================================================
# Create Template
# Admin + Lab Technician
# ==========================================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_template(
    request: CreateTemplateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    service = TemplateService(db)

    try:
        return service.create_template(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ==========================================================
# Get All Templates
# Admin + Doctor + Lab Technician
# ==========================================================

@router.get(
    "",
    response_model=list[LabTemplateResponse],
)
async def get_all_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    service = TemplateService(db)

    return service.get_all_templates()


# ==========================================================
# Get Template By Test Code
# Admin + Doctor + Lab Technician
# ==========================================================

@router.get(
    "/{test_code}",
    response_model=LabTemplateResponse,
)
async def get_template(
    test_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.DOCTOR,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    service = TemplateService(db)

    try:
        return service.get_template(test_code)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ==========================================================
# Update Template
# Admin + Lab Technician
# ==========================================================

@router.put(
    "/{test_code}",
)
async def update_template(
    test_code: str,
    request: UpdateTemplateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.LAB_TECHNICIAN,
        )
    ),
):

    service = TemplateService(db)

    try:
        return service.update_template(
            test_code,
            request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ==========================================================
# Delete Template
# Admin Only
# ==========================================================

@router.delete(
    "/{test_code}",
)
async def delete_template(
    test_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    service = TemplateService(db)

    try:
        return service.delete_template(
            test_code,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )