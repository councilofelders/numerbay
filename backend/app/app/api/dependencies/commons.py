""" Dependencies for multiple endpoints """
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.core.celery_app import celery_app


def validate_search_params(skip: int = None) -> None:
    """Validate search params"""
    if skip and skip < 0:
        raise HTTPException(
            status_code=400,
            detail="Skip must be positive",
        )


def on_round_open(db: Session) -> None:
    """On round open"""
    # call webhooks of all products
    active_orders = crud.order.get_active_orders(
        db, round_order=crud.globals.get_singleton(db=db).selling_round  # type: ignore
    )
    if active_orders is None or len(active_orders) == 0:
        return None

    active_order_products_with_webhook = {}
    for order in active_orders:
        if order.product.webhook is not None:  # type: ignore
            active_order_products_with_webhook[order.product.id] = order.product  # type: ignore

    for _, product in active_order_products_with_webhook.items():
        celery_app.send_task(
            "app.worker.trigger_webhook_for_product_task",
            args=[product.id, None],
        )
