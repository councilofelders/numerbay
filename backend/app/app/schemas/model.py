""" Data schema for Numerai model """

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel


# Shared properties
class ModelBase(BaseModel):
    name: Optional[str] = None
    tournament: Optional[int] = None
    nmr_staked: Optional[Decimal] = None
    latest_ranks: Optional[Dict] = None
    latest_reps: Optional[Dict] = None
    latest_returns: Optional[Dict] = None
    round_model_performances: Optional[List] = None
    start_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None


# Properties to receive on model creation
class ModelCreate(ModelBase):
    id: str
    name: str
    tournament: int
    owner_id: int


# Properties to receive on model update
class ModelUpdate(ModelBase):
    pass


# Properties shared by models stored in DB
class ModelInDBBase(ModelBase):
    id: str
    name: str
    tournament: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Model(ModelInDBBase):
    pass


# Properties properties stored in DB
class ModelInDB(ModelInDBBase):
    pass


# Minimal model information
class ModelMinimal(BaseModel):
    id: str
    name: Optional[str] = None
    tournament: Optional[int] = None
    start_date: Optional[datetime] = None

    class Config:
        orm_mode = True


# Summary model performance for products
class ModelSummary(BaseModel):
    name: Optional[str] = None
    tournament: Optional[int] = None
    nmr_staked: Optional[Decimal] = None
    latest_ranks: Optional[Dict] = None
    latest_reps: Optional[Dict] = None
    latest_returns: Optional[Dict] = None
    start_date: Optional[datetime] = None

    class Config:
        orm_mode = True
