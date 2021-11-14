from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, validator


# Shared properties
from app.schemas.user import PollOwner


class PollBase(BaseModel):
    date_creation: Optional[datetime] = None
    date_finish: Optional[datetime] = None
    topic: Optional[str] = None
    description: Optional[str] = None
    is_multiple: Optional[bool] = None
    max_options: Optional[int] = None
    is_anonymous: Optional[bool] = None
    is_blind: Optional[bool] = None
    is_numerai_only: Optional[bool] = None
    is_stake_predetermined: Optional[bool] = None
    weight_mode: Optional[str] = None
    options: Optional[List[Dict]] = None


# Properties to receive on poll creation
class PollCreate(PollBase):
    id: str
    date_creation: datetime
    date_finish: datetime
    topic: str
    options: List[Dict]
    owner_id: int


# Properties to receive on poll update
class PollUpdate(PollBase):
    pass


# Properties shared by models stored in DB
class PollInDBBase(PollBase):
    id: str
    topic: str

    class Config:
        orm_mode = True


# Properties to return to client
class Poll(PollInDBBase):
    owner: Optional[PollOwner] = None

    @validator("options", always=True)
    def validate_options(cls, value, values):
        print(values)
        if values.get('is_multiple', False):
            for option in value:
                option['selected'] = False
        return value


# Properties properties stored in DB
class PollInDB(PollInDBBase):
    owner_id: int
