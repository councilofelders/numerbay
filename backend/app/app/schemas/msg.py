""" Data schema for msg (used for test) """

from pydantic import BaseModel


class Msg(BaseModel):
    """Data schema for msg (used for test)"""

    msg: str
