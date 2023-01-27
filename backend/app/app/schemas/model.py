""" Data schema for Numerai model """

from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import BaseModel


# Shared properties
class ModelBase(BaseModel):
    """Base data schema for Numerai model"""

    name: Optional[str] = None
    tournament: Optional[int] = None
    nmr_staked: Optional[Decimal] = None
    stake_info: Optional[Dict] = None
    latest_ranks: Optional[Dict] = None
    latest_reps: Optional[Dict] = None
    latest_returns: Optional[Dict] = None
    round_model_performances: Optional[List] = None
    start_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None


# Properties to receive on model creation
class ModelCreate(ModelBase):
    """Create data schema for Numerai model"""

    id: str
    name: str
    tournament: int
    owner_id: int


# Properties to receive on model update
class ModelUpdate(ModelBase):
    """Update data schema for Numerai model"""


# Properties shared by models stored in DB
class ModelInDBBase(ModelBase):
    """Base database data schema for Numerai model"""

    id: str
    name: str
    tournament: int
    owner_id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Model(ModelInDBBase):
    """API data schema for Numerai model"""


# Properties properties stored in DB
class ModelInDB(ModelInDBBase):
    """Database data schema for Numerai model"""


# Minimal model information
class ModelMinimal(BaseModel):
    """Minimal API data schema for Numerai model"""

    id: str
    name: Optional[str] = None
    tournament: Optional[int] = None
    start_date: Optional[datetime] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Summary model performance for products
class ModelSummary(BaseModel):
    """API data schema for Numerai model summary"""

    id: str
    name: Optional[str] = None
    tournament: Optional[int] = None
    nmr_staked: Optional[Decimal] = None
    stake_info: Optional[Dict] = None
    latest_ranks: Optional[Dict] = None
    latest_reps: Optional[Dict] = None
    latest_returns: Optional[Dict] = None
    start_date: Optional[datetime] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
