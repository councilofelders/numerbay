""" Login endpoints """

import hashlib
import hmac
import secrets
import time
from datetime import timedelta
from typing import Any

import eth_utils
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

# from app.core.security import get_password_hash
# from app.utils import (
#     generate_password_reset_token,
#     send_reset_password_email,
#     verify_password_reset_token,
# )

router = APIRouter()


def _new_challenge(address: str) -> str:
    """Build a challenge for a wallet that has no account yet."""
    ts = str(int(time.time()))
    mac = hmac.new(
        settings.SECRET_KEY.encode(),
        f"{address.lower()}:{ts}".encode(),
        hashlib.sha256,
    ).hexdigest()[:16]
    return f"{ts}:{mac}"


def _valid_challenge(address: str, challenge: str, max_age_seconds: int = 600) -> bool:
    try:
        ts, mac = challenge.split(":", 1)
        expected = hmac.new(
            settings.SECRET_KEY.encode(),
            f"{address.lower()}:{ts}".encode(),
            hashlib.sha256,
        ).hexdigest()[:16]
        return hmac.compare_digest(mac, expected) and (
            time.time() - int(ts) <= max_age_seconds
        )
    except (TypeError, ValueError):
        return False


def _normalize_address_or_400(public_address: str) -> str:
    """Normalize a wallet address, rejecting invalid input."""
    try:
        normalized = security.normalize_public_address(public_address)
    except ValueError:
        normalized = None
    if normalized is None:
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    return normalized


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:  # pylint: disable=no-else-raise
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id,
            token_version=user.token_version,
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
        "user": user,
    }


@router.post("/login/access-token-web3", response_model=schemas.Token)
def login_access_token_web3(
    db: Session = Depends(deps.get_db),
    public_address: str = Body(...),
    signature: str = Body(...),
    nonce: str = Body(None),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    public_address = _normalize_address_or_400(public_address)
    user = crud.user.get_by_public_address(db, public_address=public_address)
    if user is None:
        if (
            nonce is None
            or not _valid_challenge(public_address, nonce)
            or not security.verify_signature(public_address, nonce, signature)
        ):
            raise HTTPException(status_code=400, detail="Incorrect signature")
        try:
            user = crud.user.create(
                db,
                obj_in=schemas.UserCreate(
                    username=public_address,
                    password=secrets.token_hex(32),
                    public_address=public_address,
                    nonce=secrets.token_hex(32),
                    is_active=True,
                ),
            )
        except IntegrityError:
            db.rollback()
            user = crud.user.get_by_public_address(db, public_address=public_address)
    else:
        try:
            user = crud.user.authenticate_web3(
                db, public_address=public_address, signature=signature
            )
        except eth_utils.exceptions.ValidationError:
            raise HTTPException(status_code=400, detail="Incorrect signature")
        if user:
            # change nonce after login
            user = crud.user.update(
                db, db_obj=user, obj_in={"nonce": secrets.token_hex(32)}
            )
    if not user:  # pylint: disable=no-else-raise
        raise HTTPException(status_code=400, detail="Incorrect signature")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id,
            token_version=user.token_version,
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
        "user": user,
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/login/nonce", response_model=schemas.Nonce)
def login_nonce(
    *,
    db: Session = Depends(deps.get_db),
    public_address: str = Body(..., embed=True),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    public_address = _normalize_address_or_400(public_address)
    user = crud.user.get_by_public_address(db, public_address=public_address)
    if user:
        # always update nonce
        crud.user.update(db, db_obj=user, obj_in={"nonce": secrets.token_hex(32)})
        return {"nonce": user.nonce}
    # no account yet: hand out a signed challenge, save nothing
    return {"nonce": _new_challenge(public_address)}


@router.get("/login/nonce", response_model=schemas.Nonce)
def login_nonce_authenticated(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    if not current_user.nonce:
        # create nonce if none
        crud.user.update(
            db, db_obj=current_user, obj_in={"nonce": secrets.token_hex(32)}
        )
    return {"nonce": current_user.nonce}


# @router.post("/password-recovery/{email}", response_model=schemas.Msg)
# def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Password Recovery
#     """
#     user = crud.user.get_by_email(db, email=email)
#
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email=email)
#     send_reset_password_email(
#         email_to=user.email, email=email, token=password_reset_token
#     )
#     return {"msg": "Password recovery email sent"}


# @router.post("/reset-password/", response_model=schemas.Msg)
# def reset_password(
#     token: str = Body(...),
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.user.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not crud.user.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}
