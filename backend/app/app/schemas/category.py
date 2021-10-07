from typing import List, Optional

from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    tournament: Optional[int] = None
    is_per_round: Optional[bool] = None


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    name: str
    slug: str


# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int
    name: str
    slug: str
    # parent: Optional['CategoryInDBBase']
    items: Optional[List["CategoryInDBBase"]]

    class Config:
        orm_mode = True


CategoryInDBBase.update_forward_refs()


# Properties to return to client
class CategoryIntermediate(CategoryInDBBase):
    parent: Optional[CategoryInDBBase]


class Category(CategoryInDBBase):
    parent: Optional[CategoryIntermediate]


Category.update_forward_refs()


# Properties properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
