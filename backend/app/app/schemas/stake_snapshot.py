from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class StakeSnapshotBase(BaseModel):
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
    date_creation: datetime
    name: str
    tournament: int


# Properties to receive on stake_snapshot update
class StakeSnapshotUpdate(StakeSnapshotBase):
    pass


# Properties shared by models stored in DB
class StakeSnapshotInDBBase(StakeSnapshotBase):
    id: str

    class Config:
        orm_mode = True


# Properties to return to client
class StakeSnapshot(StakeSnapshotInDBBase):
    pass


# Properties properties stored in DB
class StakeSnapshotInDB(StakeSnapshotInDBBase):
    pass
