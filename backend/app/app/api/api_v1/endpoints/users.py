""" Users endpoints """

import secrets
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.core.config import settings
from app.core.security import (
    normalize_public_address,
    verify_password,
    verify_signature,
)
from app.db.session import SessionLocal
from app.utils import (
    generate_email_verification_token,
    send_email_verification_email,
    verify_email_verification_token,
)

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


@router.post("/verify-email", response_model=schemas.Msg)
def verify_email(
    *,
    db: Session = Depends(deps.get_db),
    token: str = Body(..., embed=True),
) -> Any:
    """
    Confirm a pending email change with a verification token.
    """
    decoded = verify_email_verification_token(token)
    if decoded is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_id, email = decoded
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.pending_email != email:
        raise HTTPException(status_code=400, detail="Invalid token")
    existing_email_user = crud.user.get_by_email(db, email=user.pending_email)
    if existing_email_user and existing_email_user.id != user.id:
        crud.user.update(db, db_obj=user, obj_in={"pending_email": None})
        raise HTTPException(
            status_code=400,
            detail="This email address is already in use.",
        )
    try:
        crud.user.update(
            db,
            db_obj=user,
            obj_in={
                "email": user.pending_email,
                "email_verified": True,
                "pending_email": None,
            },
        )
    except IntegrityError:
        db.rollback()
        crud.user.update(db, db_obj=user, obj_in={"pending_email": None})
        raise HTTPException(
            status_code=400,
            detail="This email address is already in use.",
        )
    return {"msg": "Email verified"}


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
    current_password: str = Body(None),
    reauth_signature: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    def reauth_ok() -> bool:
        """Check that the caller proved who they are right now."""
        if current_password and current_user.hashed_password:
            if verify_password(current_password, current_user.hashed_password):
                return True
        if reauth_signature and current_user.public_address:
            if verify_signature(
                current_user.public_address,
                current_user.nonce,  # type: ignore
                reauth_signature,
            ):
                return True
        return False

    # Either username or publicAddress needs to be available
    if password is not None:
        if not reauth_ok():
            raise HTTPException(
                status_code=403,
                detail="Re-authentication required to change password",
            )
        user_in.password = password
    if username is not None and username != user_in.username:
        existing_user = crud.user.get_by_username(db, username=username)
        if existing_user:
            raise HTTPException(status_code=400, detail="This username already exists.")
        user_in.username = username
    pending_email_change = None
    if email is not None and email != current_user.email:
        if not reauth_ok():
            raise HTTPException(
                status_code=403,
                detail="Re-authentication required to change email",
            )
        existing_email_user = crud.user.get_by_email(db, email=email)
        if existing_email_user and existing_email_user.id != current_user.id:
            raise HTTPException(
                status_code=400,
                detail="This email address is already in use.",
            )
        if settings.REQUIRE_EMAIL_VERIFICATION:
            if not settings.EMAILS_ENABLED:
                raise HTTPException(
                    status_code=503,
                    detail="Email verification is required but email delivery "
                    "is not configured",
                )
            user_in.pending_email = email
            pending_email_change = email
        else:
            user_in.email = email
            user_in.email_verified = False
            user_in.pending_email = None

    # Update default receiving wallet
    if default_receiving_wallet_address is not None:
        lowered = default_receiving_wallet_address.lower()
        if lowered != (current_user.default_receiving_wallet_address or "").lower():
            if not reauth_ok():
                raise HTTPException(
                    status_code=403,
                    detail="Re-authentication required to change payout address",
                )
        user_in.default_receiving_wallet_address = lowered

    # Update socials
    user_in.social_discord = social_discord
    user_in.social_linkedin = social_linkedin
    user_in.social_twitter = social_twitter
    user_in.social_website = social_website

    # Update Numerai API key
    if numerai_api_key_public_id is not None:
        if numerai_api_key_secret is not None:
            if not reauth_ok():
                raise HTTPException(
                    status_code=403,
                    detail="Re-authentication required to change Numerai API key",
                )
            user_in.numerai_api_key_public_id = numerai_api_key_public_id
            user_in.numerai_api_key_secret = numerai_api_key_secret
            user_json = jsonable_encoder(user_in)
            user_json["id"] = current_user.id
            tmp_db = SessionLocal()
            numerai.sync_user_numerai_api(tmp_db, user_json)
    if public_address is not None and public_address == "":  # disconnect web3
        if not reauth_ok():
            raise HTTPException(
                status_code=403,
                detail="Re-authentication required to disconnect wallet",
            )
        user_in.public_address = None
        user_in.signature = None
    if public_address is not None and signature is not None:
        if not reauth_ok():
            raise HTTPException(
                status_code=403,
                detail="Re-authentication required to change wallet",
            )
        if not verify_signature(
            public_address, current_user.nonce, signature  # type: ignore
        ):
            raise HTTPException(status_code=400, detail="Invalid signature")
        try:
            normalized_address = normalize_public_address(public_address)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        if normalized_address is None:
            raise HTTPException(status_code=400, detail="Invalid wallet address")
        existing_wallet_user = crud.user.get_by_public_address(
            db, public_address=normalized_address
        )
        if existing_wallet_user and existing_wallet_user.id != current_user.id:
            raise HTTPException(
                status_code=400,
                detail="This wallet address is already linked to another account.",
            )
        new_nonce = secrets.token_hex(32)
        user_in.nonce = new_nonce
        user_in.public_address = normalized_address
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

    if reauth_signature is not None:
        user_in.nonce = secrets.token_hex(32)

    if password is not None:
        db.query(models.User).filter(models.User.id == current_user.id).update(
            {models.User.token_version: models.User.token_version + 1},
            synchronize_session=False,
        )

    try:
        user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This email address is already in use.",
        )
    if pending_email_change is not None:
        send_email_verification_email(
            email_to=pending_email_change,
            username=user.username,
            token=generate_email_verification_token(
                current_user.id, pending_email_change
            ),
        )
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
