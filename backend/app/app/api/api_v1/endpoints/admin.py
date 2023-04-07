""" Admin endpoints (admin only) """
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.api.dependencies.commons import on_round_open
from app.api.dependencies.orders import (
    get_order_weekend_round_numbers,
    send_order_confirmation_emails,
)
from app.api.deps import make_gcp_authorized_post_request
from app.core.celery_app import celery_app
from app.crud.crud_stats import calculate_stake_for_tournament, fill_round_stats
from app.models import Artifact

router = APIRouter()


@router.post("/update-daily-pricing")
def update_daily_pricing(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    users = (
        db.query(models.User).filter(not_(models.User.props["factor"].is_(None))).all()
    )
    for user in users:
        print("Updating daily pricing for user", user.username)
        try:
            user_products = crud.product.get_multi_by_owner(db, owner_id=user.id)
            for product in user_products:
                if not product.is_active:
                    continue
                for pricing_option in product.options:  # type: ignore
                    pricing_option.price = (
                        pricing_option.price * Decimal(user.props["factor"])
                    ).quantize(Decimal(".0001"), rounding=ROUND_HALF_EVEN)
            db.commit()
        except Exception as e:
            print("Error updating daily pricing for user", user.username, e)
        finally:
            db.rollback()

    return {"msg": "success!"}


@router.post("/test-webhook-auth")
def test_webhook_auth(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    endpoint: str,
    url: str,
) -> Any:
    response = make_gcp_authorized_post_request(
        endpoint,
        endpoint,
        payload={"url": url, "payload": {"test": True}},
        headers={"Content-Type": "application/json"},
    )
    print(response.status_code)
    print(response.content)
    return {"msg": "success!"}


@router.post("/fill-order-rounds")
def fill_order_rounds(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    for order_obj in crud.order.get_multi(db):
        if order_obj.rounds is not None:
            continue
        order_obj.rounds = get_order_weekend_round_numbers(
            order_obj.round_order, order_obj.quantity  # type: ignore
        )
    db.commit()
    return {"msg": "success!"}


@router.post("/on-round-open")
def invoke_round_open_hook(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    on_round_open(db)
    return {"msg": "success!"}


@router.post("/generate-stats")
def generate_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    stats = crud.stats.update_stats(db)
    return stats


@router.post("/fill-estimated-stake-stats")
def fill_estimated_stake_stats(
    *,
    db: Session = Depends(deps.get_db),
    min_round: int,
    max_round: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    instance = crud.stats.get_singleton(db)
    stats = jsonable_encoder(instance)["stats"]
    stats["estimated_stake_numerai"] = fill_round_stats(
        {
            d["round_tournament"]: d["value"]
            for d in stats.get("estimated_stake_numerai", [])
        },
        db,
        calculate_stake_for_tournament,
        min_round=min_round,
        max_round=max_round,
        tournament=8,
    )
    stats["estimated_stake_signals"] = fill_round_stats(
        {
            d["round_tournament"]: d["value"]
            for d in stats.get("estimated_stake_signals", [])
        },
        db,
        calculate_stake_for_tournament,
        min_round=min_round,
        max_round=max_round,
        tournament=11,
    )

    stats["estimated_stake"] = [
        {
            "round_tournament": stats["estimated_stake_numerai"][i]["round_tournament"],
            "value": stats["estimated_stake_numerai"][i]["value"]
            + stats["estimated_stake_signals"][i]["value"],
        }
        for i in range(len(stats["estimated_stake_numerai"]))
    ]

    crud.stats.update(
        db,
        db_obj=instance,  # type: ignore
        obj_in={
            "stats": stats,
        },
    )
    return stats


@router.post("/fill-coupon-creator")
def fill_coupon_creator(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    coupons = crud.coupon.get_multi(db, limit=None)
    for coupon in coupons:
        if coupon.applicable_product_ids and len(coupon.applicable_product_ids) > 0:
            product = crud.product.get(db, coupon.applicable_product_ids[0])
            if product:
                coupon.creator_id = product.owner_id
    db.commit()
    return {"msg": "success!"}


# @router.post("/resend-seller-order-emails")
# def resend_seller_order_emails(
#     *,
#     db: Session = Depends(deps.get_db),
#     seller_id: int,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     globals = crud.globals.update_singleton(db)
#     selling_round = globals.selling_round  # type: ignore
#
#     existing_orders = crud.order.search(
#         db,
#         role="seller",
#         current_user_id=seller_id,
#         filters={
#             "round_order": {"in": [selling_round]},
#             "state": {"in": ["pending", "confirmed"]},
#         },
#     )["data"]
#
#     for order_obj in existing_orders:
#         if settings.EMAILS_ENABLED:
#             product = order_obj.product
#             # Send seller email
#             if product.owner.email:
#                 send_new_confirmed_sale_email(
#                     email_to=product.owner.email,
#                     username=product.owner.username,
#                     round_order=order_obj.round_order,
#                     date_order=order_obj.date_order,
#                     product=product.sku,
#                     buyer=order_obj.buyer.username,
#                     from_address=order_obj.from_address,  # type: ignore
#                     to_address=order_obj.to_address,  # type: ignore
#                     transaction_hash=order_obj.transaction_hash,  # type: ignore
#                     amount=order_obj.price,
#                     currency=order_obj.currency,  # type: ignore
#                 )
#     return {"msg": "success!"}


@router.post("/resubmit-for-order")
def resubmit_for_order(  # pylint: disable=missing-function-docstring
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    order_obj = crud.order.get(db, id=order_id)
    if order_obj is not None:
        if order_obj.state == "confirmed":
            celery_app.send_task(
                "app.worker.submit_numerai_model_subtask",
                kwargs=dict(order_json=jsonable_encoder(order_obj), retry=False),
            )
    return {"msg": "success!"}


@router.post("/resend-order-emails")
def resend_order_emails(  # pylint: disable=missing-function-docstring
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    order_obj = crud.order.get(db, id=order_id)
    if order_obj is not None:
        if order_obj.state == "confirmed":
            send_order_confirmation_emails(order_obj)
    return {"msg": "success!"}


@router.post("/fill-numerai-emails")
def fill_numerai_emails(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Fill Numerai emails (for migration only).
    """
    users = (
        db.query(models.User)
        .filter(
            and_(
                models.User.email.is_(None),
                models.User.numerai_api_key_public_id.is_not(None),  # type: ignore
            )
        )
        .all()
    )
    for user in users:
        try:
            query = """
                              query {
                                account {
                                  username
                                  email
                                  id
                                  status
                                  insertedAt
                                }
                              }
                            """

            api = NumerAPI(
                public_id=user.numerai_api_key_public_id,
                secret_key=user.numerai_api_key_secret,
            )
            account = api.raw_query(query, authorization=True)["data"]["account"]
            user.email = account["email"]
        except Exception:  # pylint: disable=broad-except
            continue
    db.commit()
    return {"msg": "success!"}


@router.post("/refresh-globals-stats")
def refresh_globals_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Calculate global stats for all products (for db migration only).
    """
    crud.globals.update_stats(db)
    return {"msg": "success!"}


@router.post("/remove-failed-uploads")
def remove_failed_uploads(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Remove failed uploads (for db migration only).
    """
    artifacts = db.query(Artifact).filter(
        Artifact.object_name.is_not(None)  # type: ignore
    )
    bucket = deps.get_gcs_bucket()
    for artifact in artifacts:
        blob = bucket.blob(artifact.object_name)
        if not blob.exists():
            print(
                f"Remove artifact {artifact.object_name} for product {artifact.product.name}"
            )
            db.delete(artifact)
    db.commit()
    return {"msg": "success!"}


@router.post("/update-artifact-states")
def update_artifact_states(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Update artifact states (for db migration only).
    """
    selling_round = crud.globals.update_singleton(db).selling_round  # type: ignore

    artifacts = db.query(Artifact)
    for artifact in artifacts:
        if (
            artifact.round_tournament < selling_round
            and artifact.product.category.is_per_round
        ):
            artifact.state = "expired"
            continue

        if artifact.object_name:
            bucket = deps.get_gcs_bucket()
            blob = bucket.blob(artifact.object_name)
            if not blob.exists():
                artifact.state = "failed"
                continue
        artifact.state = "active"
    db.commit()
    return {"msg": "success!"}


# @router.post("/fill-product-readiness")
# def fill_product_readiness(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Fill product readiness (for db migration only).
#     """
#     globals = crud.globals.update_singleton(db)
#     selling_round = globals.selling_round  # type: ignore
#
#     products = db.query(Product).all()
#     for product in products:
#         artifacts = crud.artifact.get_multi_by_product_round(
#             db, product=product, round_tournament=selling_round
#         )
#         product.is_ready = len(artifacts) > 0
#     db.commit()
#     return {"msg": "success!"}
