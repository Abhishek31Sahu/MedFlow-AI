from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import hash_password
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    ChangePasswordRequest,
)

from services.practitioner_service import register_practitioner


class UserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # ==========================================================
    # Create User
    # ==========================================================

    def create_user(self, request: CreateUserRequest) -> User:

        # ------------------------------------------------------
        # Check duplicate username
        # ------------------------------------------------------

        existing_username = self.user_repository.get_by_username(
            request.username
        )

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        # ------------------------------------------------------
        # Check duplicate email
        # ------------------------------------------------------

        existing_email = self.user_repository.get_by_email(
            request.email
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        # ------------------------------------------------------
        # Create local User
        # ------------------------------------------------------

        user = User(
            username=request.username,
            email=request.email,
            hashed_password=hash_password(request.password),

            first_name=request.first_name,
            last_name=request.last_name,
            phone=request.phone,
            department=request.department,
            designation=request.designation,

            role=request.role,
            is_active=request.is_active,

            practitioner_id=None,
        )

        # ======================================================
        # DOCTOR → FHIR PRACTITIONER
        # ======================================================

        if request.role.lower() == "doctor":

            try:
                practitioner = register_practitioner(
                    first_name=request.first_name,
                    last_name=request.last_name or "",
                    gender=getattr(request, "gender", None),
                    phone=request.phone,
                    email=request.email,
                    designation=request.designation,
                )

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create FHIR Practitioner: {str(e)}",
                )

            practitioner_id = practitioner.get(
                "practitioner_id"
            )

            if not practitioner_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=(
                        "FHIR Practitioner was created "
                        "but Practitioner ID was not returned."
                    ),
                )

            # Save FHIR Practitioner ID in local user
            user.practitioner_id = practitioner_id

        # ======================================================
        # SAVE USER
        # ======================================================

        return self.user_repository.create(user)

    # ==========================================================
    # List Users
    # ==========================================================

    def get_all_users(self):

        return self.user_repository.list_all()

    # ==========================================================
    # Get User
    # ==========================================================

    def get_user(self, user_id: UUID):

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    # ==========================================================
    # Update User
    # ==========================================================

    def update_user(
        self,
        user_id: UUID,
        request: UpdateUserRequest,
    ):

        user = self.get_user(user_id)

        if request.username is not None:
            user.username = request.username

        if request.email is not None:
            user.email = request.email

        if request.first_name is not None:
            user.first_name = request.first_name

        if request.last_name is not None:
            user.last_name = request.last_name

        if request.phone is not None:
            user.phone = request.phone

        if request.department is not None:
            user.department = request.department

        if request.designation is not None:
            user.designation = request.designation

        if request.role is not None:
            user.role = request.role

        if request.is_active is not None:
            user.is_active = request.is_active

        return self.user_repository.update(user)

    # ==========================================================
    # Delete User
    # ==========================================================

    def delete_user(self, user_id: UUID):

        user = self.get_user(user_id)

        self.user_repository.delete(user)

    # ==========================================================
    # Change Password
    # ==========================================================

    def change_password(
        self,
        user_id: UUID,
        request: ChangePasswordRequest,
    ):

        user = self.get_user(user_id)

        user.hashed_password = hash_password(
            request.new_password
        )

        return self.user_repository.update(user)

    # ==========================================================
    # Activate User
    # ==========================================================

    def activate_user(self, user_id: UUID):

        user = self.get_user(user_id)

        user.is_active = True

        return self.user_repository.update(user)

    # ==========================================================
    # Deactivate User
    # ==========================================================

    def deactivate_user(self, user_id: UUID):

        user = self.get_user(user_id)

        user.is_active = False

        return self.user_repository.update(user)