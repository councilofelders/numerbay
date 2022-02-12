""" Data schema for order artifact """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class OrderArtifactBase(BaseModel):
    date: Optional[datetime] = None
    round_tournament: Optional[int] = None
    description: Optional[str] = None
    url: Optional[str] = None
    object_name: Optional[str] = None
    object_size: Optional[int] = None
    state: Optional[str] = None
    is_numerai_direct: Optional[bool] = None


# Properties to receive on order_artifact creation
class OrderArtifactCreate(OrderArtifactBase):
    id: str
    order_id: int


# Properties to receive on order_artifact update
class OrderArtifactUpdate(OrderArtifactBase):
    pass


# Properties shared by models stored in DB
class OrderArtifactInDBBase(OrderArtifactBase):
    id: str
    order_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class OrderArtifact(OrderArtifactInDBBase):
    pass


# Properties properties stored in DB
class OrderArtifactInDB(OrderArtifactInDBBase):
    pass
