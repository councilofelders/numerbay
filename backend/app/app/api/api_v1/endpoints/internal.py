"""Internal worker endpoints."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.core.async_tasks import (
    enqueue_batch_update_numerai_model_scores,
    enqueue_pending_payment_updates,
    enqueue_update_active_round,
    get_batch_update_numerai_model_scores_dedupe_key,
    get_current_scheduler_slot,
    run_async_task,
)
from app.core.config import settings

router = APIRouter(prefix="/internal", include_in_schema=False)


class AsyncTaskDispatchPayload(BaseModel):
    task: str
    args: List[Any] = Field(default_factory=list)
    kwargs: Dict[str, Any] = Field(default_factory=dict)


@router.post("/tasks/dispatch")
def dispatch_async_task(
    payload: AsyncTaskDispatchPayload,
    x_internal_task_token: str = Header(None),
) -> Dict[str, str]:
    """Execute an allowlisted internal async task."""

    _require_internal_task_token(x_internal_task_token)

    run_async_task(payload.task, args=payload.args, kwargs=payload.kwargs)
    return {"msg": "success"}


@router.post("/reconcile/payments")
def reconcile_payments(
    x_internal_task_token: str = Header(None),
) -> Dict[str, int]:
    """Queue one minute-slot payment check for all pending orders."""

    _require_internal_task_token(x_internal_task_token)

    return {"queued": enqueue_pending_payment_updates()}


@router.post("/reconcile/active-round")
def reconcile_active_round(
    x_internal_task_token: str = Header(None),
    x_cloudscheduler_scheduletime: Optional[str] = Header(
        None, alias="X-CloudScheduler-ScheduleTime"
    ),
) -> Dict[str, str]:
    """Queue one minute-slot active-round sync."""

    _require_internal_task_token(x_internal_task_token)

    enqueue_update_active_round(
        schedule_slot=_get_scheduler_slot(x_cloudscheduler_scheduletime)
    )
    return {"msg": "success"}


@router.post("/reconcile/numerai-model-scores")
def reconcile_numerai_model_scores(
    x_internal_task_token: str = Header(None),
    x_cloudscheduler_scheduletime: Optional[str] = Header(
        None, alias="X-CloudScheduler-ScheduleTime"
    ),
) -> Dict[str, str]:
    """Queue one scheduled Numerai model-scores sync."""

    _require_internal_task_token(x_internal_task_token)

    schedule_slot = _get_scheduler_slot(x_cloudscheduler_scheduletime)
    enqueue_batch_update_numerai_model_scores(
        retries=10,
        dedupe_key=get_batch_update_numerai_model_scores_dedupe_key(schedule_slot),
    )
    return {"msg": "success"}


def _require_internal_task_token(x_internal_task_token: str) -> None:
    """Validate the shared internal worker token."""

    expected_token = settings.ASYNC_WORKER_DISPATCH_TOKEN
    if not expected_token:
        raise HTTPException(status_code=503, detail="Internal task dispatch disabled")
    if x_internal_task_token != expected_token:
        raise HTTPException(status_code=403, detail="Invalid internal task token")


def _get_scheduler_slot(x_cloudscheduler_scheduletime: Optional[str]) -> str:
    """Use Cloud Scheduler's fire time when present for stable dedupe across retries."""

    if not x_cloudscheduler_scheduletime:
        return get_current_scheduler_slot()

    try:
        schedule_time = datetime.fromisoformat(
            x_cloudscheduler_scheduletime.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid Cloud Scheduler schedule time"
        ) from exc

    if schedule_time.tzinfo is None:
        schedule_time = schedule_time.replace(tzinfo=timezone.utc)

    return get_current_scheduler_slot(now=schedule_time.astimezone(timezone.utc))
