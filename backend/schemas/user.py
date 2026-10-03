from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.enums import UserRole


# ============================================================
# Create User
# ============================================================

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=30)
    department: Optional[str] = Field(None, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)

    role: UserRole = UserRole.DOCTOR
    is_active: bool = True


# ============================================================
# Update User
# ============================================================

class UpdateUserRequest(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50
    )

    email: Optional[EmailStr] = None

    first_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100
    )

    last_name: Optional[str] = Field(
        None,
        max_length=100
    )

    phone: Optional[str] = Field(
        None,
        max_length=30
    )

    department: Optional[str] = Field(
        None,
        max_length=100
    )

    designation: Optional[str] = Field(
        None,
        max_length=100
    )

    role: Optional[UserRole] = None

    is_active: Optional[bool] = None


# ============================================================
# Change Password
# ============================================================

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(
        ...,
        min_length=8
    )


# ============================================================
# User Response
# ============================================================

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr

    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None

    role: UserRole
    is_active: bool

    practitioner_id: Optional[str] = None


# ============================================================
# User List Response
# ============================================================

class UserListResponse(BaseModel):
    users: list[UserResponse]