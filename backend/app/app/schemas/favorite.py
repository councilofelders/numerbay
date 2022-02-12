""" Data schema for favorite """

from pydantic import BaseModel

from app.schemas.product import Product


# Shared properties
class FavoriteBase(BaseModel):
    """ Base data schema for favorite """


# Properties to receive on favorite creation
class FavoriteCreate(FavoriteBase):
    """ Create data schema for favorite """

    product_id: int


# Properties to receive on favorite update
class FavoriteUpdate(FavoriteBase):
    """ Update data schema for favorite """

    product_id: int


# Properties shared by models stored in DB
class FavoriteInDBBase(FavoriteBase):
    """ Base database data schema for favorite """

    id: int
    user_id: int
    product: Product

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Properties to return to client
class Favorite(FavoriteInDBBase):
    """ API data schema for favorite """


# Properties properties stored in DB
class FavoriteInDB(FavoriteInDBBase):
    """ Database data schema for favorite """
