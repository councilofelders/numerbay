""" App security functions """

import re
from datetime import datetime, timedelta
from typing import Any, Optional, Union

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils.exceptions import ValidationError
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any],
    token_version: int = 0,
    expires_delta: timedelta = None,
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "ver": token_version}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def normalize_public_address(address: str) -> Optional[str]:
    """Normalize a wallet address for storage and lookup."""
    a = (address or "").strip()
    if not a:
        return None
    if not re.fullmatch(r"0x[0-9a-fA-F]{40}", a):
        raise ValueError("Invalid wallet address")
    return a


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_signature(public_address: str, nonce: str, signature: str) -> bool:
    try:
        message_hash = encode_defunct(text=f"I am signing my one-time nonce: {nonce}")
        signer = Account.recover_message(message_hash, signature=signature)
        return signer.lower() == public_address.lower()
    except (ValueError, ValidationError):
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
