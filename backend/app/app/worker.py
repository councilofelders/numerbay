import sys
from typing import Any, Dict, Optional

from celery import group
from celery.schedules import crontab
from fastapi.encoders import jsonable_encoder
from raven import Client

from app import crud
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def tick(msg: str) -> str:
    from datetime import datetime

    print(f"Tick! The time is: {datetime.now()}, arg: {msg}")
    sys.stdout.flush()
    import time

    time.sleep(2)
    return msg


@celery_app.task  # (acks_late=True)
def update_model_subtask(user_json: Dict) -> Optional[Any]:
    db = SessionLocal()
    try:
        # Update user info
        crud.user.update_numerai_api(db, user_json)
        # Update user models
        return crud.model.update_model(db, user_json)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_models_task() -> None:
    db = SessionLocal()
    try:
        users = crud.user.search(
            db, filters={"numerai_api_key_public_id": ["any"]}, limit=None  # type: ignore
        )["data"]
        print(f"total: {len(users)}")
        # result = chord([fetch_model_subtask.s(jsonable_encoder(user), 0) for user in users],
        # commit_models_subtask.s(0)).delay()
        group(
            [update_model_subtask.s(jsonable_encoder(user)) for user in users]
        ).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def update_globals_task() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.update_singleton(db)
        crud.product.bulk_expire(db, current_round=globals.selling_round)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def update_payment_subtask(order_json: Dict) -> None:
    db = SessionLocal()
    try:
        # Update order payment
        crud.order.update_payment(db, order_json)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_payments_task() -> None:
    db = SessionLocal()
    try:
        orders = crud.order.get_multi_by_state(db, state="pending")
        print(f"total pending orders: {len(orders)}")
        group(
            [update_payment_subtask.s(jsonable_encoder(order)) for order in orders]
        ).delay()
    finally:
        db.close()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:  # type: ignore
    print("Setup Cron Tasks")
    sender.conf.beat_schedule = {
        "test_tick": {
            "task": "app.worker.tick",
            "schedule": crontab(day_of_week="wed-sun", hour=0, minute=0),
            "args": (["cron test"]),
        },
        "batch_update_models": {
            "task": "app.worker.batch_update_models_task",
            "schedule": crontab(day_of_week="wed-sun", hour=0, minute=0),
        },
        "update_globals_task": {
            "task": "app.worker.update_globals_task",
            "schedule": crontab(day_of_week="sat", hour=18, minute=5),
        },
    }
    sender.add_periodic_task(20.0, batch_update_payments_task.s(), name='batch update payments every 20 seconds')
    # todo turnkey rollout
