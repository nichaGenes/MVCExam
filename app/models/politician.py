import re
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

if TYPE_CHECKING:
    from .promise import Promise


class PoliticianBase(SQLModel):
    """Base schema สำหรับ validation"""
    id: str = Field(primary_key=True, max_length=8)
    name: str = Field(max_length=255)
    party: str = Field(max_length=255)

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not re.match(r"^[1-9]\d{7}$", v):
            raise ValueError("รหัสนักการเมืองต้องเป็นเลข 8 หลัก ขึ้นต้นด้วย 1-9")
        return v


class Politician(PoliticianBase, table=True):
    """Database table model"""
    __tablename__ = "politicians"

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    promises: List["Promise"] = Relationship(back_populates="politician")


# --- Schemas สำหรับ API Request/Response ---

class PoliticianCreate(PoliticianBase):
    pass


class PoliticianRead(PoliticianBase):
    created_at: Optional[datetime] = None