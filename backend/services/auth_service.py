from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from models.user import User
from repositories.user_repository import UserRepository

from schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenResponse,
    UserResponse,
)

from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # ==========================================================
    # LOGIN
    # ==========================================================

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:

        # ------------------------------------------------------
        # Find user
        # ------------------------------------------------------

        user = self.user_repository.get_by_username(
            request.username
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        # ------------------------------------------------------
        # Verify password
        # ------------------------------------------------------

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        # ------------------------------------------------------
        # Check account status
        # ------------------------------------------------------

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # ------------------------------------------------------
        # Generate JWT tokens
        # ------------------------------------------------------

        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = create_refresh_token(
            str(user.id)
        )

        # ------------------------------------------------------
        # Return logged-in user
        # ------------------------------------------------------

        return LoginResponse(
            message="Login successful",

            user=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,

                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                department=user.department,
                designation=user.designation,

                role=user.role,
                is_active=user.is_active,

                # FHIR Practitioner ID
                practitioner_id=user.practitioner_id,
            ),

            tokens=TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            ),
        )

    # ==========================================================
    # REFRESH TOKEN
    # ==========================================================

    async def refresh_token(self, refresh_token: str) -> TokenResponse:

    # validates signature, expiry, type == "refresh", and that sub exists
        payload = decode_refresh_token(refresh_token)

        user = self.user_repository.get_by_id(payload["sub"])

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=refresh_token,
            token_type="bearer",
        )

    # ==========================================================
    # GET CURRENT USER
    # ==========================================================

    async def get_current_user(
        self,
        user_id: UUID,
    ) -> User:

        user = self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    # ==========================================================
    # LOGOUT
    # ==========================================================

    async def logout(self):

        """
        JWT logout is handled on the frontend by
        deleting the stored tokens.

        If refresh tokens are stored in the database
        in the future, revoke/delete them here.
        """

        return {
            "message": "Logged out successfully"
        }