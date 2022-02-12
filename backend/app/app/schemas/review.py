""" Data schema for review """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import OrderBuyer


# Shared properties
class ReviewBase(BaseModel):
    """ Base data schema for review """

    created_at: Optional[datetime] = None
    round_tournament: Optional[int] = None
    rating: Optional[int] = None
    text: Optional[str] = None
    is_verified_order: Optional[bool] = None


# Properties to receive on review creation
class ReviewCreate(ReviewBase):
    """ Create data schema for review """

    round_tournament: int
    rating: int
    is_verified_order: bool
    reviewer_id: int
    product_id: int


# Properties to receive on review update
class ReviewUpdate(ReviewBase):
    """ Update data schema for review """


# Properties shared by models stored in DB
class ReviewInDBBase(ReviewBase):
    """ Base database data schema for review """

    id: int
    reviewer: OrderBuyer
    product_id: int

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Review(ReviewInDBBase):
    """ API data schema for review """


# Properties properties stored in DB
class ReviewInDB(ReviewInDBBase):
    """ Database data schema for review """
