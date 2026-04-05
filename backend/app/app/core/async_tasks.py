"""Shared async task dispatch and direct task runners."""

import base64
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional

import requests
from fastapi.encoders import jsonable_encoder
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from app.core.celery_app import celery_app
from app.core.config import settings

TASK_SEND_EMAIL = "send-email"
TASK_BATCH_UPDATE_NUMERAI_MODELS = "batch-update-numerai-models"
TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES = "batch-update-numerai-model-scores"
TASK_CHECK_NUMERAI_SUBMISSION = "check-numerai-submission"
TASK_SEND_NEW_ARTIFACT_EMAILS = "send-new-artifact-emails"
TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS = "send-new-order-artifact-emails"
TASK_TRIGGER_WEBHOOK_FOR_PRODUCT = "trigger-webhook-for-product"
TASK_UPDATE_NUMERAI_MODEL = "update-numerai-model"
TASK_UPDATE_PAYMENT = "update-payment"
TASK_UPLOAD_NUMERAI_ARTIFACT = "upload-numerai-artifact"
TASK_VALIDATE_ARTIFACT_UPLOAD = "validate-artifact-upload"


ASYNC_TASK_DEFINITIONS = {
    TASK_SEND_EMAIL: {
        "celery_task": "app.worker.send_email_task",
        "owner_setting": "ASYNC_OWNER_NOTIFICATIONS",
        "queue_setting": "GCP_TASKS_QUEUE_NOTIFICATIONS",
    },
    TASK_BATCH_UPDATE_NUMERAI_MODELS: {
        "celery_task": "app.worker.batch_update_models_task",
        "owner_setting": "ASYNC_OWNER_OPS",
        "queue_setting": "GCP_TASKS_QUEUE_OPS",
    },
    TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES: {
        "celery_task": "app.worker.batch_update_model_scores_task",
        "owner_setting": "ASYNC_OWNER_OPS",
        "queue_setting": "GCP_TASKS_QUEUE_OPS",
    },
    TASK_SEND_NEW_ARTIFACT_EMAILS: {
        "celery_task": "app.worker.send_new_artifact_emails_task",
        "owner_setting": "ASYNC_OWNER_NOTIFICATIONS",
        "queue_setting": "GCP_TASKS_QUEUE_NOTIFICATIONS",
    },
    TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS: {
        "celery_task": "app.worker.send_new_order_artifact_emails_task",
        "owner_setting": "ASYNC_OWNER_NOTIFICATIONS",
        "queue_setting": "GCP_TASKS_QUEUE_NOTIFICATIONS",
    },
    TASK_TRIGGER_WEBHOOK_FOR_PRODUCT: {
        "celery_task": "app.worker.trigger_webhook_for_product_task",
        "owner_setting": "ASYNC_OWNER_WEBHOOKS",
        "queue_setting": "GCP_TASKS_QUEUE_WEBHOOKS",
    },
    TASK_UPDATE_NUMERAI_MODEL: {
        "celery_task": "app.worker.update_model_subtask",
        "owner_setting": "ASYNC_OWNER_OPS",
        "queue_setting": "GCP_TASKS_QUEUE_OPS",
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
    TASK_VALIDATE_ARTIFACT_UPLOAD: {
        "celery_task": "app.worker.validate_artifact_upload_task",
        "owner_setting": "ASYNC_OWNER_SUBMISSIONS",
        "queue_setting": "GCP_TASKS_QUEUE_SUBMISSIONS",
    },
    TASK_CHECK_NUMERAI_SUBMISSION: {
        "celery_task": "app.worker.submit_numerai_model_subtask",
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
    dedupe_key: Optional[str] = None,
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
        dedupe_key=dedupe_key,
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


def enqueue_batch_update_numerai_models() -> Any:
    """Enqueue the Numerai model sync batch task."""

    return enqueue_async_task(TASK_BATCH_UPDATE_NUMERAI_MODELS)


def enqueue_batch_update_numerai_model_scores(
    *, retries: int = 0, delay_seconds: Optional[float] = None
) -> Any:
    """Enqueue the Numerai model scores batch task."""

    return enqueue_async_task(
        TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES,
        kwargs=dict(retries=retries),
        delay_seconds=delay_seconds,
    )


def enqueue_trigger_webhook_for_product(
    product_id: int, order_id: Optional[int] = None
) -> Any:
    """Enqueue the product webhook task."""

    return enqueue_async_task(
        TASK_TRIGGER_WEBHOOK_FOR_PRODUCT,
        args=[product_id, order_id],
    )


def enqueue_update_numerai_model(
    user_json: Dict[str, Any],
    *,
    retries: int = 0,
    delay_seconds: Optional[float] = None,
) -> Any:
    """Enqueue one Numerai model update task."""

    return enqueue_async_task(
        TASK_UPDATE_NUMERAI_MODEL,
        kwargs=dict(user_json=user_json, retries=retries),
        delay_seconds=delay_seconds,
    )


def enqueue_send_new_artifact_emails(artifact_id: int) -> Any:
    """Enqueue new artifact notification fan-out."""

    return enqueue_async_task(
        TASK_SEND_NEW_ARTIFACT_EMAILS,
        args=[artifact_id],
    )


def enqueue_send_new_order_artifact_emails(artifact_id: str) -> Any:
    """Enqueue new order artifact notification fan-out."""

    return enqueue_async_task(
        TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS,
        args=[artifact_id],
    )


def enqueue_update_payment(
    order_id: int,
    delay_seconds: Optional[float] = None,
    poll_slot: Optional[str] = None,
) -> Any:
    """Enqueue the payment update task."""

    task_kwargs: Dict[str, Any] = {}
    dedupe_key = None
    if poll_slot is not None:
        task_kwargs["poll_slot"] = poll_slot
        if settings.ASYNC_OWNER_PAYMENTS == "gcp":
            dedupe_key = get_payment_poll_dedupe_key(order_id, poll_slot)

    return enqueue_async_task(
        TASK_UPDATE_PAYMENT,
        args=[order_id],
        kwargs=task_kwargs,
        delay_seconds=delay_seconds,
        dedupe_key=dedupe_key,
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


def enqueue_validate_artifact_upload(
    artifact_id: int,
    *,
    skip_if_active: bool = True,
    delay_seconds: Optional[float] = None,
) -> Any:
    """Enqueue artifact upload validation."""

    return enqueue_async_task(
        TASK_VALIDATE_ARTIFACT_UPLOAD,
        kwargs=dict(
            artifact_id=artifact_id,
            skip_if_active=skip_if_active,
        ),
        delay_seconds=delay_seconds,
    )


def enqueue_check_numerai_submission(
    order_json: Dict[str, Any],
    *,
    retry: bool = True,
    delay_seconds: Optional[float] = None,
) -> Any:
    """Enqueue one order submission readiness check."""

    return enqueue_async_task(
        TASK_CHECK_NUMERAI_SUBMISSION,
        kwargs=dict(order_json=order_json, retry=retry),
        delay_seconds=delay_seconds,
    )


def enqueue_pending_payment_updates(poll_slot: Optional[str] = None) -> int:
    """Seed payment updates for all currently pending orders."""

    if poll_slot is None and settings.ASYNC_OWNER_PAYMENTS == "gcp":
        poll_slot = get_current_payment_reconcile_slot()
    order_ids = _get_pending_order_ids()
    for order_id in order_ids:
        enqueue_update_payment(order_id, poll_slot=poll_slot)
    return len(order_ids)


def enqueue_pending_submission_checks() -> int:
    """Seed submission readiness checks for all currently pending submission orders."""

    orders = _get_pending_submission_orders_json()
    for order_json in orders:
        enqueue_check_numerai_submission(order_json)
    return len(orders)


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
    dedupe_key: Optional[str],
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
                "body": base64.b64encode(json.dumps(payload).encode("utf-8")).decode(
                    "utf-8"
                ),
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
    if dedupe_key:
        request_body["task"]["name"] = build_cloud_task_name(
            queue_parent=queue_parent,
            task_name=task_name,
            dedupe_key=dedupe_key,
        )

    try:
        response = _get_cloud_tasks_session().post(
            f"https://cloudtasks.googleapis.com/v2/{queue_parent}/tasks",
            json=request_body,
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        if dedupe_key and exc.response is not None and exc.response.status_code == 409:
            return {"duplicate": True}
        raise


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


def _run_update_numerai_model(
    user_json: Dict[str, Any], retries: int = 0
) -> Optional[Any]:
    from app import crud
    from app.api.dependencies import numerai
    from app.db.session import run_with_db_session

    try:
        user_json_copy = user_json.copy()
        api_result = numerai.get_numerai_api_info(user_json_copy)
        user_json_copy["_api_data"] = api_result

        def update_user_and_models(db):
            user_has_valid_numerai_api = crud.user.update_numerai_api(db, user_json)

            updated_username = None
            if user_has_valid_numerai_api["success"]:
                updated_username = crud.model.update_model(db, user_json)

            if updated_username is None:
                print(f"Trying to update user {user_json['username']} without auth")
                crud.model.update_model_unauthenticated(db, user_json)

            return updated_username

        run_with_db_session(update_user_and_models)
    except Exception as exc:  # pylint: disable=broad-except
        print(
            f"Error updating model scores for user {user_json['username']}: "
            f"[{exc}], {retries} retries remaining"
        )
        if retries > 0:
            print(
                f"Retrying updating model scores for user {user_json['username']} "
                f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS} seconds"
            )
            enqueue_update_numerai_model(
                user_json,
                retries=retries - 1,
                delay_seconds=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
            )
    return None


def _run_batch_update_numerai_models() -> None:
    from app import crud
    from app.db.session import run_with_db_session

    def get_users_with_api_keys(db):
        return crud.user.search(
            db,
            filters={"numerai_api_key_public_id": ["any"]},
            limit=None,
        )["data"]

    users = run_with_db_session(get_users_with_api_keys)
    print(f"total: {len(users)}")
    for i, user in enumerate(users):
        enqueue_update_numerai_model(
            jsonable_encoder(user),
            retries=10,
            delay_seconds=i // 5,
        )
    return None


def _run_batch_update_numerai_model_scores(retries: int = 0) -> None:
    from app import crud
    from app.api.dependencies import numerai
    from app.db.session import run_with_db_session

    try:
        pipeline_status = numerai.get_numerai_pipeline_status(tournament=8)

        if pipeline_status["isScoringDay"]:
            if pipeline_status.get("resolvedAt", None):
                print("Numerai pipeline completed, update model scores...")

                users = run_with_db_session(
                    lambda db: crud.user.search(
                        db,
                        filters={"numerai_api_key_public_id": ["any"]},
                        limit=None,
                    )["data"]
                )

                print(f"total: {len(users)}")
                for i, user in enumerate(users):
                    enqueue_update_numerai_model(
                        jsonable_encoder(user),
                        retries=10,
                        delay_seconds=60 + i // 5,
                    )
            else:
                print(
                    f"Numerai pipeline not ready, checking again "
                    f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS}s"
                )
                enqueue_batch_update_numerai_model_scores(
                    retries=retries,
                    delay_seconds=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
                )
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error starting model scores update [{exc}], {retries} retries remaining")
        if retries > 0:
            print(
                f"Retrying starting model scores update "
                f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS} seconds"
            )
            enqueue_batch_update_numerai_model_scores(
                retries=retries - 1,
                delay_seconds=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
            )
    return None


def _run_send_new_artifact_emails(artifact_id: int) -> None:
    from app import crud
    from app.api.dependencies.artifacts import send_artifact_emails_for_active_orders
    from app.db.session import run_with_db_session

    if not settings.EMAILS_ENABLED:
        return None

    def send_artifact_emails(db):
        artifact = crud.artifact.get(db, id=artifact_id)
        if artifact is None:
            return None
        send_artifact_emails_for_active_orders(db, artifact)
        return None

    run_with_db_session(send_artifact_emails)
    return None


def _run_send_new_order_artifact_emails(artifact_id: str) -> None:
    from app import crud
    from app.db.session import run_with_db_session
    from app.utils import send_new_artifact_email, send_new_artifact_seller_email

    if not settings.EMAILS_ENABLED:
        return None

    def send_order_artifact_emails(db):
        artifact = crud.order_artifact.get(db, id=artifact_id)
        if artifact is None:
            return None

        order = artifact.order
        if order.buyer.email:
            send_new_artifact_email(
                email_to=order.buyer.email,
                username=order.buyer.username,
                round_order=order.round_order,
                product=order.product.sku,
                order_id=order.id,
                artifact=artifact.object_name,  # type: ignore[arg-type]
            )

        if order.product.owner.email:
            send_new_artifact_seller_email(
                email_to=order.product.owner.email,
                username=order.product.owner.username,
                round_tournament=artifact.round_tournament,  # type: ignore[arg-type]
                product=order.product.sku,
                artifact=artifact.object_name,  # type: ignore[arg-type]
            )
        return None

    run_with_db_session(send_order_artifact_emails)
    return None


def _run_update_payment(order_id: int, poll_slot: Optional[str] = None) -> None:
    del poll_slot
    _run_update_payment_in_db(order_id)
    return None


def get_current_payment_reconcile_slot(
    now: Optional[datetime] = None,
) -> str:
    """Return the current minute slot for payment reconciliation."""

    if now is None:
        now = datetime.now(timezone.utc)
    return now.astimezone(timezone.utc).strftime("%Y%m%d%H%M")


def get_payment_poll_dedupe_key(order_id: int, poll_slot: str) -> str:
    """Return a deterministic dedupe key for one order in one poll slot."""

    return f"order-{order_id}-slot-{poll_slot}"


def build_cloud_task_name(queue_parent: str, task_name: str, dedupe_key: str) -> str:
    """Return a stable Cloud Tasks task name for deduped dispatch."""

    safe_task_name = re.sub(r"[^A-Za-z0-9_-]", "-", task_name).strip("-") or "task"
    safe_dedupe_key = re.sub(r"[^A-Za-z0-9_-]", "-", dedupe_key).strip("-")
    return f"{queue_parent}/tasks/{safe_task_name}-{safe_dedupe_key}"


def _get_pending_order_ids() -> List[int]:
    from app import crud
    from app.db.session import run_with_db_session

    def get_pending_order_ids(db):
        orders = crud.order.get_multi_by_state(db, state="pending")
        return [order.id for order in orders]

    return run_with_db_session(get_pending_order_ids)


def _get_pending_submission_orders_json() -> List[Dict[str, Any]]:
    from app import crud
    from app.db.session import run_with_db_session

    def get_pending_submission_orders_json(db):
        orders = crud.order.get_pending_submission_orders(
            db,
            round_order=crud.globals.update_singleton(db).selling_round,
        )
        return [jsonable_encoder(order) for order in orders]

    return run_with_db_session(get_pending_submission_orders_json)


def _run_update_payment_in_db(order_id: int) -> None:
    from app.api.dependencies.orders import update_payment
    from app.db.session import run_with_db_session

    run_with_db_session(lambda db: update_payment(db, order_id))


def _send_failed_autosubmit_emails_in_db(order_id: int, artifact_name: str) -> None:
    from app import crud
    from app.api.dependencies.orders import send_failed_autosubmit_emails
    from app.db.session import run_with_db_session

    def send_failed_emails(db):
        order_obj = crud.order.get(db, id=order_id)
        if order_obj is None:
            return None
        send_failed_autosubmit_emails(
            order_obj=order_obj,
            artifact_name=artifact_name,
        )
        return None

    run_with_db_session(send_failed_emails)


def _run_check_numerai_submission(
    order_json: Dict[str, Any], retry: bool = True
) -> Optional[Any]:
    from app import crud
    from app.api import deps
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        order_id = order_json["id"]
        print(f"Checking artifact submission for order [{order_id}]")

        product = crud.product.get(db=db, id=order_json["product_id"])
        site_globals = crud.globals.update_singleton(db)
        selling_round = site_globals.selling_round  # type: ignore

        artifacts = crud.artifact.get_multi_by_product_round(
            db, product=product, round_tournament=selling_round  # type: ignore[arg-type]
        )

        csv_artifacts = [
            artifact
            for artifact in artifacts or []
            if artifact.object_name and artifact.object_name.endswith(".csv")
        ]
        if not csv_artifacts:
            if site_globals.is_doing_round_rollover:
                print(
                    f"Submission for order [{order_id}] interrupted due to round closing"
                )
                return None
            if retry:
                print(
                    f"No csv artifact for order [{order_id}], "
                    f"trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
                )
                enqueue_check_numerai_submission(
                    order_json,
                    delay_seconds=settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS,
                )
            else:
                print(f"No csv artifact for order [{order_id}]")
            return None

        csv_artifact = csv_artifacts[-1]
        bucket = deps.get_gcs_bucket()
        blob = bucket.blob(csv_artifact.object_name)  # type: ignore[arg-type]
        if not blob.exists():
            if retry:
                print(
                    f"Csv artifact for order [{order_id}] not yet uploaded, "
                    f"trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
                )
                enqueue_check_numerai_submission(
                    order_json,
                    delay_seconds=settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS,
                )
            else:
                print(f"Csv artifact for order [{order_id}] not yet uploaded")
            return None

        buyer = crud.user.get(db, id=order_json["buyer_id"])
        if buyer is None:
            return None

        print(
            f"Uploading csv artifact {csv_artifact.object_name} for order {order_id}"
        )
        enqueue_upload_numerai_artifact(
            order_id=order_id,
            object_name=csv_artifact.object_name,  # type: ignore[arg-type]
            model_id=order_json["submit_model_id"],
            numerai_api_key_public_id=buyer.numerai_api_key_public_id,
            numerai_api_key_secret=buyer.numerai_api_key_secret,
            tournament=product.model.tournament,  # type: ignore[union-attr]
            version=1,
        )
        return None
    finally:
        db.close()


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
            order_obj.submit_state = "failed"
            db.add(order_obj)
            db.commit()
            db.refresh(order_obj)

        run_with_db_session(mark_submission_failed)
        _send_failed_autosubmit_emails_in_db(order_id, object_name)
        return None
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error uploading artifact: {str(exc)}")

        def mark_submission_failed(db):
            order_obj = crud.order.get(db, id=order_id)
            if order_obj is None:
                return None
            order_obj.submit_state = "failed"
            db.add(order_obj)
            db.commit()
            db.refresh(order_obj)

        run_with_db_session(mark_submission_failed)
        _send_failed_autosubmit_emails_in_db(order_id, object_name)
        return None


def _run_validate_artifact_upload(
    artifact_id: int,
    skip_if_active: bool = True,
) -> None:
    from app import crud
    from app.api import deps
    from app.db.session import run_with_db_session
    from app.utils import send_failed_artifact_seller_email

    def validate_artifact(db):
        artifact = crud.artifact.get(db, id=artifact_id)

        if skip_if_active and artifact and artifact.state == "active":
            print(
                f"Artifact {artifact_id} {artifact.object_name} already validated, skipping"
            )
            return None

        if artifact is None or not artifact.object_name:
            return None

        bucket = deps.get_gcs_bucket()
        blob = bucket.blob(artifact.object_name)
        if not blob.exists():
            print(f"Artifact {artifact_id} {artifact.object_name} not uploaded, deleting")

            if settings.EMAILS_ENABLED and artifact.product.owner.email:
                send_failed_artifact_seller_email(
                    email_to=artifact.product.owner.email,
                    username=artifact.product.owner.username,
                    round_tournament=artifact.round_tournament,  # type: ignore[arg-type]
                    product=artifact.product.sku,
                    artifact=artifact.object_name,
                )

            crud.artifact.update(db, db_obj=artifact, obj_in={"state": "failed"})
            return None

        print(
            f"Artifact {artifact_id} {artifact.object_name} is valid, "
            f"searching for orders to upload..."
        )

        selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
        orders = crud.order.get_active_orders(db, round_order=selling_round)
        for order in orders:
            if not order.submit_model_id:
                continue
            if order.product_id != artifact.product_id:
                continue

            print(f"Uploading csv artifact {artifact.object_name} for order {order.id}")
            enqueue_upload_numerai_artifact(
                order_id=order.id,
                object_name=artifact.object_name,
                model_id=order.submit_model_id,
                numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,
                numerai_api_key_secret=order.buyer.numerai_api_key_secret,
                tournament=order.product.model.tournament,
                version=1,
            )

        print(f"Mark artifact {artifact.id} as active and send out email notifications")
        enqueue_send_new_artifact_emails(artifact.id)
        crud.artifact.update(db, db_obj=artifact, obj_in={"state": "active"})

        product = crud.product.get(db, id=artifact.product_id)
        if product and not product.is_ready:
            crud.product.update(db, db_obj=product, obj_in={"is_ready": True})
        return None

    run_with_db_session(validate_artifact)
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
    TASK_BATCH_UPDATE_NUMERAI_MODELS: _run_batch_update_numerai_models,
    TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES: _run_batch_update_numerai_model_scores,
    TASK_CHECK_NUMERAI_SUBMISSION: _run_check_numerai_submission,
    TASK_SEND_EMAIL: _run_send_email,
    TASK_SEND_NEW_ARTIFACT_EMAILS: _run_send_new_artifact_emails,
    TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS: _run_send_new_order_artifact_emails,
    TASK_TRIGGER_WEBHOOK_FOR_PRODUCT: _run_trigger_webhook_for_product,
    TASK_UPDATE_NUMERAI_MODEL: _run_update_numerai_model,
    TASK_UPDATE_PAYMENT: _run_update_payment,
    TASK_UPLOAD_NUMERAI_ARTIFACT: _run_upload_numerai_artifact,
    TASK_VALIDATE_ARTIFACT_UPLOAD: _run_validate_artifact_upload,
}
