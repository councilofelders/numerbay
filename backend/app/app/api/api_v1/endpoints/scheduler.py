import asyncio
import secrets
import sys
from datetime import datetime
from typing import Any, List

from app.core.apscheduler import scheduler
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


async def tick():
    print('Tick! The time is: %s' % datetime.now())
    sys.stdout.flush()
    await asyncio.sleep(1)


@router.get('/get_schedules')
def get_schedules(
    # *,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    schedules = []
    for job in scheduler.get_jobs():
        schedules.append({'id': str(job.id), 'frequency': str(job.trigger), 'next_run': str(job.next_run_time)})
    return schedules


@router.post('/trigger-job/numerai-models')
def trigger_job_numerai_models(
    # *,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    scheduler.get_job(job_id ="batch_update_models").modify(next_run_time=datetime.now())
    return {"msg": "success!"}
