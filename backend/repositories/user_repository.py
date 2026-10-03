from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    def __init__(self, db: Session):
        print("UserRepository db:", type(db))
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        result = self.db.execute(
            select(User).where(User.id == str(user_id))
        )
        return result.scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        result = self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        result = self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    def list_all(self) -> list[User]:
        result = self.db.execute(
            select(User).order_by(User.username)
        )
        return result.scalars().all()

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()