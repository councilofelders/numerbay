""" Scheduler endpoints (admin only) """

from typing import Any

from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/get_schedules")
def get_schedules(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Get schedules"""
    i = celery_app.control.inspect()
    return {
        "scheduled": i.scheduled(),
        "active": i.active(),
        "reserved": i.reserved(),
        "registered": i.registered(),
    }


@router.post("/test")
def add_job_test(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add test job"""
    celery_app.send_task("app.worker.tick", args=["add"])

    return {"msg": "success!"}


@router.post("/numerai-models")
def add_job_numerai_models(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add Numerai models job"""
    celery_app.send_task("app.worker.batch_update_models_task")

    return {"msg": "success!"}


@router.post("/numerai-model-scores")
def add_job_numerai_model_scores(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add Numerai model scores job"""
    celery_app.send_task("app.worker.batch_update_model_scores_task")

    return {"msg": "success!"}


@router.post("/round-rollover")
def add_job_round_rollover(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add round rollover job"""
    celery_app.send_task("app.worker.update_round_rollover")

    return {"msg": "success!"}


@router.post("/payments")
def add_job_payments(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add payments job"""
    celery_app.send_task("app.worker.batch_update_payments_task")

    return {"msg": "success!"}


@router.post("/submit")
def add_job_submit_numerai_models(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add submit Numerai models job"""
    celery_app.send_task("app.worker.batch_submit_numerai_models_task")

    return {"msg": "success!"}


@router.post("/stake")
def add_job_validate_numerai_models_stake(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add validate Numerai models stake job"""
    celery_app.send_task("app.worker.batch_validate_numerai_models_stake_task")

    return {"msg": "success!"}


@router.post("/stake-snapshot")
def add_job_update_stake_snapshots(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add update stake snapshots job"""
    celery_app.send_task("app.worker.batch_update_stake_snapshots")

    return {"msg": "success!"}


@router.post("/update-polls")
def add_job_update_polls(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add update polls job"""
    celery_app.send_task("app.worker.batch_update_polls")

    return {"msg": "success!"}


@router.post("/prune-storage")
def add_job_prune_storage(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add prune storage job"""
    celery_app.send_task("app.worker.batch_prune_storage")

    return {"msg": "success!"}


@router.post("/artifact-reminder")
def add_job_artifact_reminder(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add artifact reminder job"""
    celery_app.send_task("app.worker.send_order_artifact_upload_reminder_emails_task")

    return {"msg": "success!"}


@router.post("/webhook/{id}")
def trigger_webhook_for_product(
    *,
    id: int,  # pylint: disable=W0622
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Trigger webhook for product"""
    celery_app.send_task("app.worker.trigger_webhook_for_product_task", args=[id])

    return {"msg": "success!"}


@router.post("/product-stats")
def add_job_batch_update_product_sales_stats(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add delivery rate job"""
    celery_app.send_task("app.worker.batch_update_product_sales_stats")

    return {"msg": "success!"}
