""" Data schema for category """

from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    """Base data schema for category"""

    name: Optional[str] = None
    slug: Optional[str] = None
    tournament: Optional[int] = None
    is_per_round: Optional[bool] = None
    is_submission: Optional[bool] = None
    is_per_model: Optional[bool] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    """Create data schema for category"""

    name: str
    slug: str


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    """Update data schema for category"""


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    """Base database data schema for category"""

    id: int
    name: str
    slug: str
    # parent: Optional['CategoryInDBBase']
    items: Optional[List["CategoryInDBBase"]]

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# CategoryInDBBase.update_forward_refs()


# Properties to return to client
class CategoryIntermediate(CategoryInDBBase):
    """Nested API data schema for category"""

    parent: Optional[CategoryInDBBase]


class Category(CategoryInDBBase):
    """API data schema for category"""

    # parent: Optional[CategoryIntermediate]
    parent_id: Optional[int]


# Category.update_forward_refs()


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    """Database data schema for category"""
