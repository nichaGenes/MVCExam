from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .promise import Promise


class CampaignBase(SQLModel):
    id: str = Field(primary_key=True, max_length=20)
    year: int
    district: str


class Campaign(CampaignBase, table=True):
    __tablename__ = "campaigns"

    promises: List["Promise"] = Relationship(back_populates="campaign")


class CampaignCreate(CampaignBase):
    pass


class CampaignRead(CampaignBase):
    pass
