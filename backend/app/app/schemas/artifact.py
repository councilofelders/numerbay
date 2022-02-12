""" Data schema for artifact """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ArtifactBase(BaseModel):
    date: Optional[datetime] = None
    round_tournament: Optional[int] = None
    description: Optional[str] = None
    url: Optional[str] = None
    object_name: Optional[str] = None
    object_size: Optional[int] = None
    state: Optional[str] = None


# Properties to receive on artifact creation
class ArtifactCreate(ArtifactBase):
    product_id: int


# Properties to receive on artifact update
class ArtifactUpdate(ArtifactBase):
    pass


# Properties shared by models stored in DB
class ArtifactInDBBase(ArtifactBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Artifact(ArtifactInDBBase):
    pass


# Properties properties stored in DB
class ArtifactInDB(ArtifactInDBBase):
    pass
