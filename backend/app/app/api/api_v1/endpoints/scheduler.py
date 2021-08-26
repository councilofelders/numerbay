import asyncio
import secrets
import sys
from datetime import datetime
from typing import Any, List

from .models import batch_update_models
from app.core.apscheduler import scheduler
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get('/get_schedules')
def get_schedules(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    schedules = []
    for job in scheduler.get_jobs():
        schedules.append({'id': str(job.id), 'frequency': str(job.trigger), 'next_run': str(job.next_run_time)})
    return schedules


# @scheduler.scheduled_job('interval', id='test', seconds=5)
def tick():
    print('Tick! The time is: %s' % datetime.now())
    sys.stdout.flush()


@router.post('/add-job/test')
def add_job_test(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.add_job(tick, 'interval', seconds=5, id='test', replace_existing=True)
    return {"msg": f"success! {scheduler.running}"}


@router.delete('/trigger-job/test-scheduler')
def delete_job_test(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.remove_job('test')
    return {"msg": "success!"}


@router.post('/add-job/numerai-models')
def add_job_numerai_models(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.add_job(batch_update_models, 'cron', day_of_week='wed-sun', id='batch_update_models', replace_existing=True)
    return {"msg": f"success! {scheduler.running}"}


@router.post('/trigger-job/numerai-models')
def trigger_job_numerai_models(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.get_job(job_id ="batch_update_models").modify(next_run_time=datetime.now())
    return {"msg": "success!"}


@router.delete('/trigger-job/numerai-models')
def delete_job_numerai_models(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.remove_job('batch_update_models')
    return {"msg": "success!"}
