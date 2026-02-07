import enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=255)
    role: UserRole = Field(
        sa_column=Column(Enum(UserRole, name="user_role", create_type=False)),
        default=UserRole.USER,
    )
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


# --- Schemas ---

class UserLogin(SQLModel):
    username: str
    password: str