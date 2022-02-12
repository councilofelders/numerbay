""" Data schema for favorite """

from pydantic import BaseModel

from app.schemas.product import Product


# Shared properties
class FavoriteBase(BaseModel):
    pass


# Properties to receive on favorite creation
class FavoriteCreate(FavoriteBase):
    product_id: int


# Properties to receive on favorite update
class FavoriteUpdate(FavoriteBase):
    product_id: int


# Properties shared by models stored in DB
class FavoriteInDBBase(FavoriteBase):
    id: int
    user_id: int
    product: Product

    class Config:
        orm_mode = True


# Properties to return to client
class Favorite(FavoriteInDBBase):
    pass


# Properties properties stored in DB
class FavoriteInDB(FavoriteInDBBase):
    pass
