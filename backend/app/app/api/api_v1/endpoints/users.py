""" Users endpoints """

import secrets
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.core.security import verify_signature
from app.db.session import SessionLocal

# from app.core.config import settings
# from app.utils import send_new_account_email

router = APIRouter()


# @router.get("/", response_model=List[schemas.User])
# def read_users(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Retrieve users.
#     """
#     users = crud.user.get_multi(db, skip=skip, limit=limit)
#     return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    if (
        user_in.username is None
        or user_in.username == ""
        or user_in.password is None
        or user_in.password == ""
    ):
        raise HTTPException(
            status_code=400,
            detail="Please specify username and password",
        )

    user = crud.user.get_by_username(db, username=user_in.username)  # type: ignore
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_in.nonce = secrets.token_hex(32)
    user = crud.user.create(db, obj_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email,
    #         password=user_in.password   # type: ignore
    #     )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(  # pylint: disable=too-many-locals
    *,
    db: Session = Depends(deps.get_db),
    username: str = Body(None),
    password: str = Body(None),
    email: EmailStr = Body(None),
    default_receiving_wallet_address: str = Body(None),
    social_discord: str = Body(None),
    social_linkedin: str = Body(None),
    social_twitter: str = Body(None),
    social_website: str = Body(None),
    public_address: str = Body(None),
    numerai_api_key_public_id: str = Body(None),
    numerai_api_key_secret: str = Body(None),
    signature: str = Body(None),
    public_key: str = Body(None),
    encrypted_private_key: str = Body(None),
    factor: float = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    # Either username or publicAddress needs to be available
    if password is not None:
        user_in.password = password
    if username is not None and username != user_in.username:
        existing_user = crud.user.get_by_username(db, username=username)
        if existing_user:
            raise HTTPException(status_code=400, detail="This username already exists.")
        user_in.username = username
    if email is not None:
        user_in.email = email

    # Update default receiving wallet
    if default_receiving_wallet_address is not None:
        user_in.default_receiving_wallet_address = default_receiving_wallet_address

    # Update socials
    user_in.social_discord = social_discord
    user_in.social_linkedin = social_linkedin
    user_in.social_twitter = social_twitter
    user_in.social_website = social_website

    # Update Numerai API key
    if numerai_api_key_public_id is not None:
        if numerai_api_key_secret is not None:
            user_in.numerai_api_key_public_id = numerai_api_key_public_id
            user_in.numerai_api_key_secret = numerai_api_key_secret
            user_json = jsonable_encoder(user_in)
            user_json["id"] = current_user.id
            tmp_db = SessionLocal()
            numerai.sync_user_numerai_api(tmp_db, user_json)
    if public_address is not None and public_address == "":  # disconnect web3
        user_in.public_address = None
        user_in.signature = None
    if public_address is not None and signature is not None:
        if not verify_signature(
            public_address, current_user.nonce, signature  # type: ignore
        ):
            raise HTTPException(status_code=400, detail="Invalid signature")
        new_nonce = secrets.token_hex(32)
        user_in.nonce = new_nonce
        user_in.public_address = public_address
        user_in.signature = signature
    if public_key is not None and encrypted_private_key is not None:
        user_in.public_key_v2 = public_key
        user_in.encrypted_private_key_v2 = encrypted_private_key

        # change public keys for existing active orders
        selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        orders = crud.order.get_user_active_orders(
            db, round_order=selling_round, buyer_id=current_user.id
        )
        for order in orders:
            if order.buyer_public_key is not None:
                order.buyer_public_key = public_key

    # Update user props
    if not user_in.props:
        user_in.props = {}
    if factor is not None:
        user_in.props["factor"] = factor

    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),  # pylint: disable=W0613
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/sync-numerai", response_model=schemas.User)
def sync_user_numerai(  # pylint: disable=too-many-locals
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Sync user with Numerai API"""
    user_json = jsonable_encoder(current_user)
    numerai.sync_user_numerai_api(db, user_json)
    return crud.user.get(db, current_user.id)


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user_by_id(
#     user_id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Get a specific user by id.
#     """
#     user = crud.user.get(db, id=user_id)
#     if user == current_user:
#         return user
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return user


# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.UserUpdate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update a user.
#     """
#     user = crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system",
#         )
#     user = crud.user.update(db, db_obj=user, obj_in=user_in)
#     return user
