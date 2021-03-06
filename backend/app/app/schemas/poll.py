""" Data schema for poll """

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional

import pandas as pd
from pydantic import BaseModel, root_validator

# Shared properties
from app.schemas.user import GenericOwner


class PollBase(BaseModel):
    """Base data schema for poll"""

    date_finish: Optional[date] = None
    description: Optional[str] = None
    is_blind: Optional[bool] = None


class PollOption(BaseModel):
    """API Data schema for poll option"""

    value: int
    text: str


# Properties to receive on poll creation
class PollCreate(PollBase):
    """Create data schema for poll"""

    id: Optional[str] = None
    date_creation: Optional[datetime] = None
    date_finish: date
    topic: str
    is_multiple: bool
    max_options: Optional[int] = None
    is_anonymous: Optional[bool] = None
    weight_mode: Optional[str] = None
    is_stake_predetermined: Optional[bool] = None
    stake_basis_round: Optional[int] = None
    min_stake: Optional[Decimal] = None
    min_rounds: Optional[Decimal] = None
    clip_low: Optional[Decimal] = None
    clip_high: Optional[Decimal] = None
    options: List[PollOption]
    owner_id: Optional[int] = None


# Properties to receive on poll update
class PollUpdate(PollBase):
    """Update data schema for poll"""

    options: Optional[List[PollOption]] = None


# Properties shared by models stored in DB
class PollInDBBase(PollBase):
    """Base database data schema for poll"""

    id: str
    date_creation: datetime
    topic: str
    is_finished: Optional[bool] = None
    is_multiple: bool
    max_options: Optional[int] = None
    is_anonymous: Optional[bool] = None
    weight_mode: Optional[str] = None
    is_stake_predetermined: Optional[bool] = None
    stake_basis_round: Optional[int] = None
    min_stake: Optional[Decimal] = None
    min_rounds: Optional[Decimal] = None
    clip_low: Optional[Decimal] = None
    clip_high: Optional[Decimal] = None
    options: List[Dict]

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Poll(PollInDBBase):
    """API data schema for poll"""

    owner: Optional[GenericOwner] = None
    has_voted: Optional[bool] = False

    @root_validator(pre=True)
    def set_votes(cls, values):  # type: ignore
        """Set votes"""
        if not values["is_blind"] or values["is_finished"]:
            votes = values.get("votes", None)
            if votes:
                votes_df = pd.DataFrame(
                    {
                        "option": [v.option for v in votes],
                        "weight": [v.weight_basis for v in votes],
                    }
                )
                vote_counts = votes_df.groupby("option").sum()["weight"].to_dict()
                for option, count in vote_counts.items():
                    values["options"][option]["votes"] = count
        return values

    # @validator("options", always=True)
    # def validate_options(cls, value, values):
    #     print(values)
    #     if values.get('is_multiple', False) and 'selected' not in values:
    #         for option in value:
    #             option['selected'] = False
    #     return value


# Properties properties stored in DB
class PollInDB(PollInDBBase):
    """Database data schema for poll"""

    owner_id: int
