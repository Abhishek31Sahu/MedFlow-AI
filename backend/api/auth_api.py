from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    MessageResponse,
    UserResponse,
)
from core.security import get_user_id


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

security = HTTPBearer()


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    print("get_auth_service received:", type(db), id(db))
    return AuthService(db)

# --------------------------------------------------
# Login
# --------------------------------------------------

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(request)


# --------------------------------------------------
# Refresh Token
# --------------------------------------------------

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_token(
        request.refresh_token
    )


# --------------------------------------------------
# Logout
# --------------------------------------------------

@router.post(
    "/logout",
    response_model=MessageResponse,
)
async def logout(
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout()

    return MessageResponse(
        message="Logged out successfully"
    )


# --------------------------------------------------
# Current User
# --------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
):
    token = credentials.credentials

    user_id = get_user_id(token)

    user = await auth_service.get_current_user(user_id)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )