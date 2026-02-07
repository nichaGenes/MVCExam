from datetime import date, datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .promise import Promise


class PromiseUpdateBase(SQLModel):
    id: str = Field(primary_key=True, max_length=20)
    promise_id: str = Field(foreign_key="promises.id", max_length=20)
    update_date: date
    detail: str


class PromiseUpdate(PromiseUpdateBase, table=True):
    __tablename__ = "promise_updates"

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    promise: Optional["Promise"] = Relationship(back_populates="updates")


# --- Schemas ---

class PromiseUpdateCreate(SQLModel):
    """Schema สำหรับฟอร์มเพิ่มความคืบหน้า (id จะ generate อัตโนมัติ)"""
    detail: str


class PromiseUpdateRead(PromiseUpdateBase):
    created_at: Optional[datetime] = None