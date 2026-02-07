import enum
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, Enum

if TYPE_CHECKING:
    from .politician import Politician
    from .campaign import Campaign
    from .promise_update import PromiseUpdate


class PromiseStatus(str, enum.Enum):
    NOT_STARTED = "ยังไม่เริ่ม"
    IN_PROGRESS = "กำลังดำเนินการ"
    DISAPPEARED = "เงียบหาย"


class PromiseBase(SQLModel):
    id: str = Field(primary_key=True, max_length=20)
    politician_id: str = Field(foreign_key="politicians.id", max_length=8)
    campaign_id: str = Field(foreign_key="campaigns.id", max_length=20)
    description: str
    announced_date: date
    status: PromiseStatus = Field(
        sa_column=Column(Enum(PromiseStatus, name="promise_status", create_type=False)),
        default=PromiseStatus.NOT_STARTED,
    )


class Promise(PromiseBase, table=True):
    __tablename__ = "promises"

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    # Relationships
    politician: Optional["Politician"] = Relationship(back_populates="promises")
    campaign: Optional["Campaign"] = Relationship(back_populates="promises")
    updates: List["PromiseUpdate"] = Relationship(back_populates="promise")

    def can_update(self) -> bool:
        """Business Rule: คำสัญญาที่ 'เงียบหาย' ไม่สามารถอัปเดตได้"""
        return self.status != PromiseStatus.DISAPPEARED


# --- Schemas ---

class PromiseCreate(PromiseBase):
    pass


class PromiseRead(PromiseBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None