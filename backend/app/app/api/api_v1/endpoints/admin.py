import functools
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core.celery_app import celery_app
from app.core.config import settings
from app.models import Artifact, Order, Product
from app.utils import send_new_confirmed_sale_email, send_order_confirmed_email

router = APIRouter()


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
def resubmit_for_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
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
def resend_order_emails(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    order_obj = crud.order.get(db, id=order_id)
    if order_obj is not None:
        if order_obj.state == "confirmed":
            if settings.EMAILS_ENABLED:
                product = order_obj.product
                # Send seller email
                if product.owner.email:
                    send_new_confirmed_sale_email(
                        email_to=product.owner.email,
                        username=product.owner.username,
                        round_order=order_obj.round_order,
                        date_order=order_obj.date_order,
                        product=product.sku,
                        buyer=order_obj.buyer.username,
                        from_address=order_obj.from_address,  # type: ignore
                        to_address=order_obj.to_address,  # type: ignore
                        transaction_hash=order_obj.transaction_hash,  # type: ignore
                        amount=order_obj.price,
                        currency=order_obj.currency,  # type: ignore
                    )

                # Send buyer email
                if order_obj.buyer.email:
                    send_order_confirmed_email(
                        email_to=order_obj.buyer.email,
                        username=order_obj.buyer.username,
                        round_order=order_obj.round_order,
                        date_order=order_obj.date_order,
                        product=product.sku,
                        from_address=order_obj.from_address,  # type: ignore
                        to_address=order_obj.to_address,  # type: ignore
                        transaction_hash=order_obj.transaction_hash,  # type: ignore
                        amount=order_obj.price,
                        currency=order_obj.currency,  # type: ignore
                    )
    return {"msg": "success!"}


@router.post("/fill-numerai-emails")
def fill_numerai_emails(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
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
        except Exception:
            continue
    db.commit()
    return {"msg": "success!"}


@router.post("/refresh-globals-stats")
def refresh_globals_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Calculate global stats for all products (for db migration only).
    """
    crud.globals.update_stats(db)
    return {"msg": "success!"}


@router.post("/refresh-sales-stats")
def refresh_sales_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Calculate sales stats for all products (for db migration only).
    """
    products = db.query(Product).all()
    for product in products:
        query_filters = [Order.product_id == product.id, Order.state == "confirmed"]
        query_filter = functools.reduce(lambda a, b: and_(a, b), query_filters)
        orders = db.query(Order).filter(query_filter).order_by(desc(Order.id)).all()
        if orders and len(orders) > 0:
            product.total_num_sales = len(orders)
            product.last_sale_price = orders[0].price
            if len(orders) > 1:
                product.last_sale_price_delta = (
                    product.last_sale_price - orders[1].price
                )
    db.commit()
    return {"msg": "success!"}


@router.post("/remove-failed-uploads")
def remove_failed_uploads(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Remove failed uploads (for db migration only).
    """
    artifacts = db.query(Artifact).filter(Artifact.object_name.is_not(None))  # type: ignore
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
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update artifact states (for db migration only).
    """
    globals = crud.globals.update_singleton(db)
    selling_round = globals.selling_round  # type: ignore

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
