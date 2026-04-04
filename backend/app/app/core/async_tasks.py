"""Shared async task dispatch and direct task runners."""

import base64
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional

import requests
from fastapi.encoders import jsonable_encoder
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from app.core.celery_app import celery_app
from app.core.config import settings

TASK_SEND_EMAIL = "send-email"
TASK_TRIGGER_WEBHOOK_FOR_PRODUCT = "trigger-webhook-for-product"
TASK_UPDATE_PAYMENT = "update-payment"
TASK_UPLOAD_NUMERAI_ARTIFACT = "upload-numerai-artifact"


ASYNC_TASK_DEFINITIONS = {
    TASK_SEND_EMAIL: {
        "celery_task": "app.worker.send_email_task",
        "owner_setting": "ASYNC_OWNER_NOTIFICATIONS",
        "queue_setting": "GCP_TASKS_QUEUE_NOTIFICATIONS",
    },
    TASK_TRIGGER_WEBHOOK_FOR_PRODUCT: {
        "celery_task": "app.worker.trigger_webhook_for_product_task",
        "owner_setting": "ASYNC_OWNER_WEBHOOKS",
        "queue_setting": "GCP_TASKS_QUEUE_WEBHOOKS",
    },
    TASK_UPDATE_PAYMENT: {
        "celery_task": "app.worker.update_payment_subtask",
        "owner_setting": "ASYNC_OWNER_PAYMENTS",
        "queue_setting": "GCP_TASKS_QUEUE_PAYMENTS",
    },
    TASK_UPLOAD_NUMERAI_ARTIFACT: {
        "celery_task": "app.worker.upload_numerai_artifact_task",
        "owner_setting": "ASYNC_OWNER_SUBMISSIONS",
        "queue_setting": "GCP_TASKS_QUEUE_SUBMISSIONS",
    },
}


def enqueue_async_task(
    task_name: str,
    *,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
    delay_seconds: Optional[float] = None,
) -> Any:
    """Send an async task to the currently configured owner."""

    definition = ASYNC_TASK_DEFINITIONS.get(task_name)
    if definition is None:
        raise ValueError(f"Unsupported async task: {task_name}")

    task_args = list(args or [])
    task_kwargs = dict(kwargs or {})
    owner = getattr(settings, definition["owner_setting"])
    if owner == "celery":
        celery_kwargs: Dict[str, Any] = {
            "args": task_args,
            "kwargs": task_kwargs,
        }
        if delay_seconds is not None:
            celery_kwargs["countdown"] = delay_seconds
        return celery_app.send_task(definition["celery_task"], **celery_kwargs)

    return _enqueue_cloud_task(
        task_name=task_name,
        queue_name=getattr(settings, definition["queue_setting"]),
        args=task_args,
        kwargs=task_kwargs,
        delay_seconds=delay_seconds,
    )


def enqueue_send_email(
    *,
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Optional[Dict[str, Any]] = None,
) -> Any:
    """Enqueue the generic email task."""

    return enqueue_async_task(
        TASK_SEND_EMAIL,
        kwargs=dict(
            email_to=email_to,
            subject_template=subject_template,
            html_template=html_template,
            environment=environment or {},
        ),
    )


def enqueue_trigger_webhook_for_product(
    product_id: int, order_id: Optional[int] = None
) -> Any:
    """Enqueue the product webhook task."""

    return enqueue_async_task(
        TASK_TRIGGER_WEBHOOK_FOR_PRODUCT,
        args=[product_id, order_id],
    )


def enqueue_update_payment(
    order_id: int, delay_seconds: Optional[float] = None
) -> Any:
    """Enqueue the payment update task."""

    return enqueue_async_task(
        TASK_UPDATE_PAYMENT,
        args=[order_id],
        delay_seconds=delay_seconds,
    )


def enqueue_upload_numerai_artifact(
    *,
    order_id: int,
    object_name: str,
    model_id: str,
    numerai_api_key_public_id: str,
    numerai_api_key_secret: str,
    tournament: int = 8,
    version: int = 1,
) -> Any:
    """Enqueue Numerai artifact upload."""

    return enqueue_async_task(
        TASK_UPLOAD_NUMERAI_ARTIFACT,
        kwargs=dict(
            order_id=order_id,
            object_name=object_name,
            model_id=model_id,
            numerai_api_key_public_id=numerai_api_key_public_id,
            numerai_api_key_secret=numerai_api_key_secret,
            tournament=tournament,
            version=version,
        ),
    )


def enqueue_pending_payment_updates() -> int:
    """Seed payment updates for all currently pending orders."""

    order_ids = _get_pending_order_ids()
    for order_id in order_ids:
        enqueue_update_payment(order_id)
    return len(order_ids)


def run_async_task(
    task_name: str,
    *,
    args: Optional[List[Any]] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) -> Any:
    """Run the task body directly in-process."""

    task_runner = TASK_RUNNERS.get(task_name)
    if task_runner is None:
        raise ValueError(f"Unsupported async task: {task_name}")
    return task_runner(*(args or []), **(kwargs or {}))


def _enqueue_cloud_task(
    *,
    task_name: str,
    queue_name: str,
    args: List[Any],
    kwargs: Dict[str, Any],
    delay_seconds: Optional[float],
) -> Dict[str, Any]:
    worker_url = settings.ASYNC_WORKER_DISPATCH_URL
    if not worker_url:
        raise RuntimeError("ASYNC_WORKER_DISPATCH_URL must be set for GCP async tasks")
    if not settings.GCP_SERVICE_ACCOUNT_INFO:
        raise RuntimeError("GCP_SERVICE_ACCOUNT_INFO must be set for GCP async tasks")
    if not settings.ASYNC_WORKER_DISPATCH_TOKEN:
        raise RuntimeError(
            "ASYNC_WORKER_DISPATCH_TOKEN must be set for GCP async tasks"
        )

    payload = jsonable_encoder(
        {
            "task": task_name,
            "args": args,
            "kwargs": kwargs,
        }
    )
    request_body = {
        "task": {
            "httpRequest": {
                "httpMethod": "POST",
                "url": str(worker_url),
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": base64.b64encode(
                    json.dumps(payload).encode("utf-8")
                ).decode("utf-8"),
            }
        }
    }

    request_body["task"]["httpRequest"]["headers"][
        "X-Internal-Task-Token"
    ] = settings.ASYNC_WORKER_DISPATCH_TOKEN

    worker_service_account = settings.ASYNC_WORKER_SERVICE_ACCOUNT_EMAIL
    if worker_service_account:
        request_body["task"]["httpRequest"]["oidcToken"] = {
            "serviceAccountEmail": worker_service_account,
            "audience": str(worker_url),
        }

    if delay_seconds is not None:
        scheduled_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
        request_body["task"]["scheduleTime"] = scheduled_at.isoformat().replace(
            "+00:00", "Z"
        )

    queue_parent = (
        f"projects/{settings.GCP_PROJECT}/locations/{settings.GCP_TASKS_LOCATION}"
        f"/queues/{queue_name}"
    )
    response = _get_cloud_tasks_session().post(
        f"https://cloudtasks.googleapis.com/v2/{queue_parent}/tasks",
        json=request_body,
    )
    response.raise_for_status()
    return response.json()


def _get_cloud_tasks_session() -> AuthorizedSession:
    service_account_info = json.loads(settings.GCP_SERVICE_ACCOUNT_INFO)  # type: ignore
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return AuthorizedSession(credentials)


def _run_send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = None,
) -> None:
    from app.utils import send_email

    send_email(
        email_to=email_to,
        subject_template=subject_template,
        html_template=html_template,
        environment=environment or {},
    )


def _run_update_payment(order_id: int) -> None:
    _run_update_payment_in_db(order_id)
    if settings.ASYNC_OWNER_PAYMENTS != "gcp":
        return None

    if _get_order_state(order_id) == "pending":
        enqueue_update_payment(
            order_id,
            delay_seconds=settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
        )
    return None


def _get_pending_order_ids() -> List[int]:
    from app import crud
    from app.db.session import run_with_db_session

    def get_pending_order_ids(db):
        orders = crud.order.get_multi_by_state(db, state="pending")
        return [order.id for order in orders]

    return run_with_db_session(get_pending_order_ids)


def _run_update_payment_in_db(order_id: int) -> None:
    from app.api.dependencies.orders import update_payment
    from app.db.session import run_with_db_session

    run_with_db_session(lambda db: update_payment(db, order_id))


def _get_order_state(order_id: int) -> Optional[str]:
    from app import crud
    from app.db.session import run_with_db_session

    def get_order_state(db):
        order = crud.order.get(db, id=order_id)
        return order.state if order else None

    return run_with_db_session(get_order_state)


def _run_upload_numerai_artifact(
    order_id: int,
    object_name: str,
    model_id: str,
    numerai_api_key_public_id: str,
    numerai_api_key_secret: str,
    tournament: int = 8,
    version: int = 1,
) -> Optional[Any]:
    from app import crud
    from app.api import deps
    from app.api.dependencies import numerai
    from app.api.dependencies.order_artifacts import generate_gcs_signed_url
    from app.api.dependencies.orders import (
        ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY,
        clear_order_confirmation_side_effect_complete,
        send_failed_autosubmit_emails,
    )
    from app.db.session import run_with_db_session

    def mark_order_queued(db):
        order = crud.order.get(db=db, id=order_id)
        if not order:
            print(f"Order {order_id} not found, skipped")
            return None
        return crud.order.update(db, db_obj=order, obj_in={"submit_state": "queued"})

    order = run_with_db_session(mark_order_queued)
    if order is None:
        return None

    try:
        url = generate_gcs_signed_url(
            bucket=deps.get_gcs_bucket(),
            object_name=object_name,
            action="GET",
            expiration_minutes=settings.ARTIFACT_DOWNLOAD_URL_EXPIRE_MINUTES,
            is_upload=False,
        )

        submission_auth = numerai.generate_numerai_submission_url(
            object_name=object_name,
            model_id=model_id,
            tournament=tournament,
            numerai_api_key_public_id=numerai_api_key_public_id,
            numerai_api_key_secret=numerai_api_key_secret,
        )

        file_stream = requests.get(url, stream=True)
        requests.put(
            submission_auth["url"], data=file_stream.content, stream=True
        ).raise_for_status()

        submission_id = numerai.validate_numerai_submission(
            object_name=submission_auth["filename"],
            model_id=model_id,
            tournament=tournament,
            numerai_api_key_public_id=numerai_api_key_public_id,
            numerai_api_key_secret=numerai_api_key_secret,
        )

        if submission_id:
            def mark_submission_completed(db):
                order_obj = crud.order.get(db, id=order_id)
                crud.order.update(
                    db,
                    db_obj=order_obj,  # type: ignore
                    obj_in={
                        "submit_state": "completed",
                        "last_submit_round": crud.globals.get_singleton(  # type: ignore
                            db=db
                        ).selling_round,
                    },
                )

            run_with_db_session(mark_submission_completed)
            return submission_id

        def mark_submission_failed(db):
            order_obj = crud.order.get(db, id=order_id)
            if order_obj is None:
                return None
            clear_order_confirmation_side_effect_complete(
                db,
                order_obj,
                ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY,
            )
            order_obj.submit_state = "failed"
            db.add(order_obj)
            db.commit()
            db.refresh(order_obj)

        run_with_db_session(mark_submission_failed)
        send_failed_autosubmit_emails(order_obj=order, artifact_name=object_name)  # type: ignore
        return None
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error uploading artifact: {str(exc)}")

        def mark_submission_failed(db):
            order_obj = crud.order.get(db, id=order_id)
            if order_obj is None:
                return None
            clear_order_confirmation_side_effect_complete(
                db,
                order_obj,
                ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY,
            )
            order_obj.submit_state = "failed"
            db.add(order_obj)
            db.commit()
            db.refresh(order_obj)

        run_with_db_session(mark_submission_failed)
        send_failed_autosubmit_emails(order_obj=order, artifact_name=object_name)  # type: ignore
        return None


def _run_trigger_webhook_for_product(
    product_id: int, order_id: Optional[int] = None
) -> None:
    from app import crud
    from app.api.deps import make_gcp_authorized_post_request
    from app.db.session import SessionLocal
    from app.utils import send_failed_webhook_email, send_succeeded_webhook_email

    if not settings.WEBHOOK_ENABLED:
        return None

    db = SessionLocal()
    try:
        site_globals = crud.globals.update_singleton(db)
        selling_round = site_globals.selling_round  # type: ignore
        if site_globals.active_round != selling_round:
            return None

        product = crud.product.get(db, id=product_id)
        if not product or not product.webhook:
            return None

        date_str = datetime.now().isoformat()
        response = make_gcp_authorized_post_request(
            settings.GCP_WEBHOOK_FUNCTION,  # type: ignore
            settings.GCP_WEBHOOK_FUNCTION,  # type: ignore
            payload={
                "url": product.webhook,
                "payload": {
                    "date": date_str,
                    "product_id": product.id,
                    "product_category": product.category.slug,  # type: ignore
                    "product_name": product.name,
                    "product_full_name": product.sku,
                    "model_id": product.model_id,
                    "tournament": product.category.tournament,  # type: ignore
                    "order_id": order_id,
                    "round_tournament": selling_round,
                },
            },
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            send_failed_webhook_email(
                email_to=product.owner.email,  # type: ignore
                username=product.owner.username,
                date=date_str,
                product=product.sku,
            )
            print(
                f"Webhook for {product.sku} ({product.id}) "
                f"returned an error {response.status_code}"
            )
            return None

        send_succeeded_webhook_email(
            email_to=product.owner.email,  # type: ignore
            username=product.owner.username,
            date=date_str,
            product=product.sku,
        )
        print(f"Webhook for {product.sku} ({product.id}) succeeded")
    finally:
        db.close()
    return None


TASK_RUNNERS: Dict[str, Callable[..., Any]] = {
    TASK_SEND_EMAIL: _run_send_email,
    TASK_TRIGGER_WEBHOOK_FOR_PRODUCT: _run_trigger_webhook_for_product,
    TASK_UPDATE_PAYMENT: _run_update_payment,
    TASK_UPLOAD_NUMERAI_ARTIFACT: _run_upload_numerai_artifact,
}
