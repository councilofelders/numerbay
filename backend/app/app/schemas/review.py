from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import OrderBuyer


# Shared properties
class ReviewBase(BaseModel):
    created_at: Optional[datetime] = None
    round_tournament: Optional[int] = None
    rating: Optional[int] = None
    text: Optional[str] = None
    is_verified_order: Optional[bool] = None


# Properties to receive on review creation
class ReviewCreate(ReviewBase):
    round_tournament: int
    rating: int
    is_verified_order: bool
    reviewer_id: int
    product_id: int


# Properties to receive on review update
class ReviewUpdate(ReviewBase):
    pass


# Properties shared by models stored in DB
class ReviewInDBBase(ReviewBase):
    id: int
    reviewer: OrderBuyer
    product_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Review(ReviewInDBBase):
    pass


# Properties properties stored in DB
class ReviewInDB(ReviewInDBBase):
    pass
