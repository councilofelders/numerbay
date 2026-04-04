"""Internal task dispatch endpoints."""

from typing import Any, Dict, List

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.core.async_tasks import run_async_task
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

    expected_token = settings.ASYNC_WORKER_DISPATCH_TOKEN
    if not expected_token:
        raise HTTPException(status_code=503, detail="Internal task dispatch disabled")
    if x_internal_task_token != expected_token:
        raise HTTPException(status_code=403, detail="Invalid internal task token")

    run_async_task(payload.task, args=payload.args, kwargs=payload.kwargs)
    return {"msg": "success"}
