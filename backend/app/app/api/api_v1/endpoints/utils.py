""" Utils endpoints (admin only) """
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic.networks import EmailStr, HttpUrl

from app import models, schemas
from app.api import deps
from app.api.deps import make_gcp_authorized_post_request
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import send_test_email

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.post("/test-product-webhook/")
def test_product_webhook(
    url: HttpUrl = Body(..., embed=True),
    current_user: models.User = Depends(
        deps.get_current_active_user
    ),  # pylint: disable=W0613
) -> Any:
    """
    Test product webhook.
    """
    response = make_gcp_authorized_post_request(
        settings.GCP_WEBHOOK_FUNCTION,  # type: ignore
        settings.GCP_WEBHOOK_FUNCTION,  # type: ignore
        payload={
            "url": url,
            "payload": {
                "date": datetime.now().isoformat(),
                "product_id": 1,
                "product_category": "numerai-predictions",
                "product_name": "myproduct",
                "product_full_name": "numerai-predictions-myproduct",
                "model_id": "adabxxx-3acf-470e-8733-e4283261xxxx",
                "tournament": 8,
                "order_id": None,
                "round_tournament": 326,
            },
        },
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        return {"status_code": 200, "content": "Webhook test successful"}
    raise HTTPException(
        status_code=400,
        detail="Webhook test failed",
    )
