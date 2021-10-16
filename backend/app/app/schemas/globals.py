from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class GlobalsBase(BaseModel):
    active_round: Optional[int] = None
    selling_round: Optional[int] = None
    is_doing_round_rollover: Optional[bool] = None
    total_num_products: Optional[int] = None
    total_num_sales: Optional[int] = None
    total_sales_nmr: Optional[Decimal] = None


# Properties to receive via API on creation
class GlobalsCreate(GlobalsBase):
    pass


# Properties to receive via API on update
class GlobalsUpdate(GlobalsBase):
    pass


class GlobalsInDBBase(GlobalsBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Globals(GlobalsInDBBase):
    pass


# Additional properties stored in DB
class GlobalsInDB(GlobalsInDBBase):
    pass
