from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from models.enums import UserRole


# ==========================================================
# Register Request
# ==========================================================

class RegisterRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
    )


# ==========================================================
# Login Request
# ==========================================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ==========================================================
# Refresh Token Request
# ==========================================================

class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ==========================================================
# Token Response
# ==========================================================

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ==========================================================
# User Response
# ==========================================================

class UserResponse(BaseModel):

    id: str

    username: str

    email: EmailStr

    first_name: str

    last_name: Optional[str] = None

    phone: Optional[str] = None

    department: Optional[str] = None

    designation: Optional[str] = None

    role: UserRole

    is_active: bool

    # FHIR Practitioner ID
    practitioner_id: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================================
# Login Response
# ==========================================================

class LoginResponse(BaseModel):

    message: str

    user: UserResponse

    tokens: TokenResponse


# ==========================================================
# Generic Message Response
# ==========================================================

class MessageResponse(BaseModel):
    message: str