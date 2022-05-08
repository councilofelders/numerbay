""" Data schema for globals """

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class GlobalsBase(BaseModel):
    """Base data schema for globals"""

    active_round: Optional[int] = None
    selling_round: Optional[int] = None
    is_doing_round_rollover: Optional[bool] = None
    total_num_products: Optional[int] = None
    total_num_sales: Optional[int] = None
    total_qty_sales: Optional[int] = None
    total_sales_nmr: Optional[Decimal] = None


# Properties to receive via API on creation
class GlobalsCreate(GlobalsBase):
    """Create data schema for globals"""


# Properties to receive via API on update
class GlobalsUpdate(GlobalsBase):
    """Update data schema for globals"""


class GlobalsInDBBase(GlobalsBase):
    """Base database data schema for globals"""

    id: Optional[int] = None

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


# Additional properties to return via API
class Globals(GlobalsInDBBase):
    """API data schema for globals"""


# Additional properties stored in DB
class GlobalsInDB(GlobalsInDBBase):
    """Database data schema for globals"""
