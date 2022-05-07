""" Data schema for stake snapshot """

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class StakeSnapshotBase(BaseModel):
    """Base data schema for stake snapshot"""

    date_creation: Optional[datetime] = None
    round_tournament: Optional[int] = None
    name: Optional[str] = None
    tournament: Optional[int] = None
    nmr_staked: Optional[Decimal] = None
    return_13_weeks: Optional[Decimal] = None
    return_52_weeks: Optional[Decimal] = None
    payout_pending: Optional[Decimal] = None
    model_id: Optional[str] = None


# Properties to receive on stake_snapshot creation
class StakeSnapshotCreate(StakeSnapshotBase):
    """Create data schema for stake snapshot"""

    date_creation: datetime
    name: str
    tournament: int


# Properties to receive on stake_snapshot update
class StakeSnapshotUpdate(StakeSnapshotBase):
    """Update data schema for stake snapshot"""


# Properties shared by models stored in DB
class StakeSnapshotInDBBase(StakeSnapshotBase):
    """Base database data schema for stake snapshot"""

    id: str

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class StakeSnapshot(StakeSnapshotInDBBase):
    """API data schema for stake snapshot"""


# Properties properties stored in DB
class StakeSnapshotInDB(StakeSnapshotInDBBase):
    """Database data schema for stake snapshot"""
