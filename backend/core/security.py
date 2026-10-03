from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from database.database import get_db
from models.enums import UserRole
from models.user import User


# ==========================================================
# Password Context
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ==========================================================
# HTTP Bearer Security
# ==========================================================

security = HTTPBearer()


# ==========================================================
# Password Hashing
# ==========================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# ACCESS TOKEN
# ==========================================================

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:

    # ------------------------------------------
    # Calculate expiration
    # ------------------------------------------

    if expires_delta:

        expire = (
            datetime.now(timezone.utc)
            + expires_delta
        )

    else:

        expire = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

    # ------------------------------------------
    # Access token payload
    # ------------------------------------------

    payload = {
        "sub": subject,
        "type": "access",
        "exp": expire,
    }

    # ------------------------------------------
    # Encode JWT
    # ------------------------------------------

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# ==========================================================
# REFRESH TOKEN
# ==========================================================

def create_refresh_token(
    subject: str,
) -> str:

    # ------------------------------------------
    # Refresh token should live longer
    # ------------------------------------------

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    # ------------------------------------------
    # Refresh token payload
    # ------------------------------------------

    payload = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
    }

    # ------------------------------------------
    # Encode JWT
    # ------------------------------------------

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# ==========================================================
# DECODE ACCESS TOKEN
# ==========================================================

def decode_token(
    token: str,
):
    """
    Decode and validate an ACCESS token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ],
        )

        # --------------------------------------
        # Ensure token is an access token
        # --------------------------------------

        if payload.get("type") != "access":

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # --------------------------------------
        # Ensure subject exists
        # --------------------------------------

        if not payload.get("sub"):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID missing from token",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        return payload

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


# ==========================================================
# DECODE REFRESH TOKEN
# ==========================================================

def decode_refresh_token(
    token: str,
):
    """
    Decode and validate a REFRESH token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ],
        )

        # --------------------------------------
        # Ensure token is a refresh token
        # --------------------------------------

        if payload.get("type") != "refresh":

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        # --------------------------------------
        # Ensure subject exists
        # --------------------------------------

        if not payload.get("sub"):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID missing from refresh token",
                headers={
                    "WWW-Authenticate": "Bearer"
                },
            )

        return payload

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


# ==========================================================
# GET USER ID FROM ACCESS TOKEN
# ==========================================================

def get_user_id(
    token: str,
) -> str:

    payload = decode_token(
        token
    )

    user_id = payload.get(
        "sub"
    )

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID missing from token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user_id


# ==========================================================
# GET CURRENT USER
# ==========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(
        get_db
    ),
) -> User:

    # ------------------------------------------
    # Get bearer token
    # ------------------------------------------

    token = credentials.credentials

    # ------------------------------------------
    # Get user ID from access token
    # ------------------------------------------

    user_id = get_user_id(
        token
    )

    # ------------------------------------------
    # Fetch user from database
    # ------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    # ------------------------------------------
    # Check active status
    # ------------------------------------------

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


# ==========================================================
# ROLE-BASED ACCESS CONTROL
# ==========================================================

def require_roles(
    *allowed_roles: UserRole,
):

    def role_checker(
        current_user: User = Depends(
            get_current_user
        ),
    ) -> User:

        # --------------------------------------
        # Convert database role to enum
        # --------------------------------------

        try:

            user_role = UserRole(
                current_user.role
            )

        except ValueError:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid user role",
            )

        # --------------------------------------
        # Check permission
        # --------------------------------------

        if user_role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission "
                    "to access this resource"
                ),
            )

        return current_user

    return role_checker