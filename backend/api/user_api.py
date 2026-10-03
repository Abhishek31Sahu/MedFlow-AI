from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.security import require_roles
from database.database import get_db
from models.enums import UserRole
from models.user import User

from schemas.auth import MessageResponse
from schemas.user import (
    ChangePasswordRequest,
    CreateUserRequest,
    UpdateUserRequest,
    UserListResponse,
    UserResponse,
)

from services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ==========================================================
# Create User
# Admin only
# ==========================================================

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return service.create_user(request)


# ==========================================================
# Get All Users
# Admin only
# ==========================================================

@router.get(
    "",
    response_model=UserListResponse,
)
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    users = service.get_all_users()

    return UserListResponse(
        users=users
    )


# ==========================================================
# Get User
# Admin only
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return service.get_user(user_id)


# ==========================================================
# Update User
# Admin only
# ==========================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return service.update_user(
        user_id,
        request,
    )


# ==========================================================
# Delete User
# Admin only
# ==========================================================

@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    service.delete_user(user_id)

    return MessageResponse(
        message="User deleted successfully"
    )


# ==========================================================
# Change Password
# Admin only
# ==========================================================

@router.patch(
    "/{user_id}/password",
    response_model=UserResponse,
)
async def change_password(
    user_id: UUID,
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return await service.change_password(
        user_id,
        request,
    )


# ==========================================================
# Activate User
# Admin only
# ==========================================================

@router.patch(
    "/{user_id}/activate",
    response_model=UserResponse,
)
async def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return await service.activate_user(
        user_id
    )


# ==========================================================
# Deactivate User
# Admin only
# ==========================================================

@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
async def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):
    service = UserService(db)

    return await service.deactivate_user(
        user_id
    )