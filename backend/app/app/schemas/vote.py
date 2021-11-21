from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class VoteBase(BaseModel):
    date_vote: Optional[datetime] = None
    option: Optional[int] = None
    weight_basis: Optional[Decimal] = None
    voter_id: Optional[str] = None
    voter_address: Optional[str] = None
    poll_id: Optional[str] = None


# Properties to receive on vote creation
class VoteCreate(VoteBase):
    date_vote: datetime
    option: int
    voter_id: str
    poll_id: str


# Properties to receive on vote update
class VoteUpdate(VoteBase):
    pass


# Properties shared by models stored in DB
class VoteInDBBase(VoteBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Vote(VoteInDBBase):
    pass


# Properties properties stored in DB
class VoteInDB(VoteInDBBase):
    pass
