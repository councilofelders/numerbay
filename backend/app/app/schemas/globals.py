from typing import Optional

from pydantic import BaseModel


# Shared properties
class GlobalsBase(BaseModel):
    active_round: Optional[int] = None
    selling_round: Optional[bool] = True


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
