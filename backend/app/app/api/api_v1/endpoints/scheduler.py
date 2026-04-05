""" Scheduler endpoints (admin only) """

from typing import Any

from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core.async_tasks import (
    enqueue_batch_update_numerai_model_scores,
    enqueue_batch_update_numerai_models,
    enqueue_pending_payment_updates,
    enqueue_pending_submission_checks,
    enqueue_trigger_webhook_for_product,
)
from app.ops.jobs import run_job

router = APIRouter()


@router.post("/numerai-models")
def add_job_numerai_models(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add Numerai models job"""
    enqueue_batch_update_numerai_models()

    return {"msg": "success!"}


@router.post("/numerai-model-scores")
def add_job_numerai_model_scores(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add Numerai model scores job"""
    enqueue_batch_update_numerai_model_scores()

    return {"msg": "success!"}


@router.post("/payments")
def add_job_payments(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add payments job"""
    return {"queued": enqueue_pending_payment_updates()}


@router.post("/submit")
def add_job_submit_numerai_models(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add submit Numerai models job"""
    enqueue_pending_submission_checks()

    return {"msg": "success!"}


@router.post("/stake")
def add_job_validate_numerai_models_stake(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add validate Numerai models stake job"""
    run_job("validate-numerai-models-stake")

    return {"msg": "success!"}


@router.post("/stake-snapshot")
def add_job_update_stake_snapshots(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add update stake snapshots job"""
    run_job("stake-snapshots")

    return {"msg": "success!"}


@router.post("/update-polls")
def add_job_update_polls(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add update polls job"""
    run_job("polls")

    return {"msg": "success!"}


@router.post("/prune-storage")
def add_job_prune_storage(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add prune storage job"""
    run_job("prune-storage")

    return {"msg": "success!"}


@router.post("/artifact-reminder")
def add_job_artifact_reminder(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add artifact reminder job"""
    run_job("artifact-reminders")

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
    enqueue_trigger_webhook_for_product(id)

    return {"msg": "success!"}


@router.post("/product-stats")
def add_job_batch_update_product_sales_stats(
    *,
    current_user: models.User = Depends(
        deps.get_current_active_superuser
    ),  # pylint: disable=W0613
) -> Any:
    """Add delivery rate job"""
    run_job("product-sales-stats")

    return {"msg": "success!"}
