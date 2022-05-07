""" Data schema for auth token """

from typing import Optional

from pydantic import BaseModel

from .user import User


class Token(BaseModel):
    """Base data schema for auth token"""

    access_token: str
    token_type: str
    user: User


class TokenPayload(BaseModel):
    """API data schema for auth token"""

    sub: Optional[int] = None


class Nonce(BaseModel):
    """API data schema for nonce"""

    nonce: str
