from typing import Any

from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core.celery_app import celery_app


router = APIRouter()


@router.get('/get_schedules')
def get_schedules(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    i = celery_app.control.inspect()
    return {'scheduled': i.scheduled(), 'active': i.active(), 'reserved': i.reserved(), 'registered': i.registered()}


@router.post('/test')
def add_job_test(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    celery_app.send_task("app.worker.tick", args=["add"])

    return {"msg": "success!"}


@router.post('/numerai-models')
def add_job_numerai_models(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    celery_app.send_task("app.worker.batch_update_models_task")

    return {"msg": "success!"}

