""" Utils endpoints (admin only) """
from datetime import datetime
from typing import Any

import requests
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic.networks import EmailStr, HttpUrl

from app import models, schemas
from app.api import deps
from app.core.celery_app import celery_app
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
    response = requests.post(
        url,
        json={
            "date": datetime.now().isoformat(),
            "product_id": 1,
            "product_category": "numerai-predictions",
            "product_name": "myproduct",
            "product_full_name": "numerai-predictions-myproduct",
            "model_id": "adabxxx-3acf-470e-8733-e4283261xxxx",
            "tournament": 8,
        },
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        return {"status_code": response.status_code, "content": response.text}
    raise HTTPException(
        status_code=response.status_code, detail=response.text,
    )
