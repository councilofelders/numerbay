""" Dependencies for multiple endpoints """
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.models import Product


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
    products_with_webhook = (
        db.query(Product).where(Product.webhook.is_not(None)).all()  # type: ignore
    )
    for product in products_with_webhook:
        celery_app.send_task(
            "app.worker.trigger_webhook_for_product_task",
            args=[product.id, None],
        )
