import asyncio
import secrets
import sys
from datetime import datetime
from typing import Any, List

# from .models import batch_update_models
# from app.core.apscheduler import scheduler
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.celery_app import celery_app
# from app.worker import tick

router = APIRouter()


@router.get('/get_schedules')
def get_schedules(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    i = celery_app.control.inspect()
    return {'scheduled': i.scheduled(), 'active': i.active(), 'reserved': i.reserved(), 'registered': i.registered()}


# @scheduler.scheduled_job('interval', id='test', seconds=5)
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#     sys.stdout.flush()


@router.post('/test')
def add_job_test(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    celery_app.send_task("app.worker.tick", args=["add"])

    return {"msg": "success!"}


# @router.delete('/trigger-job/test-scheduler')
# def delete_job_test(
#     *,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     scheduler.remove_job('test')
#     return {"msg": "success!"}


@router.post('/numerai-models')
def add_job_numerai_models(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    celery_app.send_task("app.worker.batch_update_models_task")

    return {"msg": "success!"}


# @router.post('/trigger-job/numerai-models')
# def trigger_job_numerai_models(
#     *,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     scheduler.get_job(job_id ="batch_update_models").modify(next_run_time=datetime.now())
#     return {"msg": "success!"}


# @router.delete('/trigger-job/numerai-models')
# def delete_job_numerai_models(
#     *,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     scheduler.remove_job('batch_update_models')
#     return {"msg": "success!"}
