""" Data schema for stats """

from typing import Dict, Optional

from pydantic import BaseModel


# Shared properties
class StatsBase(BaseModel):
    """Base data schema for stats"""

    stats: Optional[Dict] = None


# Properties to receive via API on creation
class StatsCreate(StatsBase):
    """Create data schema for stats"""


# Properties to receive via API on update
class StatsUpdate(StatsBase):
    """Update data schema for stats"""


class StatsInDBBase(StatsBase):
    """Base database data schema for stats"""

    id: Optional[int] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Additional properties to return via API
class Stats(StatsInDBBase):
    """API data schema for stats"""


# Additional properties stored in DB
class StatsInDB(StatsInDBBase):
    """Database data schema for stats"""
