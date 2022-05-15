""" Data schema for artifact """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ArtifactBase(BaseModel):
    """Base data schema for artifact"""

    date: Optional[datetime] = None
    round_tournament: Optional[int] = None
    object_name: Optional[str] = None
    object_size: Optional[int] = None
    state: Optional[str] = None


# Properties to receive on artifact creation
class ArtifactCreate(ArtifactBase):
    """Create data schema for artifact"""

    product_id: int


# Properties to receive on artifact update
class ArtifactUpdate(ArtifactBase):
    """Update data schema for artifact"""


# Properties shared by models stored in DB
class ArtifactInDBBase(ArtifactBase):
    """Base database data schema for artifact"""

    id: int
    product_id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Artifact(ArtifactInDBBase):
    """API data schema for artifact"""


# Properties properties stored in DB
class ArtifactInDB(ArtifactInDBBase):
    """Database data schema for artifact"""
