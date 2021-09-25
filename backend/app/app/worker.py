import sys
from datetime import datetime, timezone
import pandas as pd
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


@celery_app.task  # (acks_late=True) # todo deprecate old global update to new rollover
def update_globals_task() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.update_singleton(db)
        crud.product.bulk_expire(db, current_round=globals.selling_round)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def update_round_rollover() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.get_singleton(db)

        active_round = crud.globals.get_numerai_active_round()
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()
        # next_round_open_time = pd.to_datetime(active_round["closeTime"]).to_pydatetime()

        active_round_number = active_round["number"]
        print(f'UTC time: {utc_time}, round open: {open_time}, round close: {close_staking_time}, round: {active_round_number}')

        if open_time <= utc_time <= close_staking_time:  # new round opened and active
            print('Activities freezed due to round rollover')
            crud.globals.update(db, db_obj=globals, obj_in={'is_doing_round_rollover': True})  # freeze activities
            celery_app.send_task("app.worker.update_round_rollover", countdown=settings.ROUND_ROLLOVER_POLL_FREQUENCY_SECONDS)  # try again soon
        else:  # current round closed for staking, start selling next round, unfreeze activities
            if active_round_number == globals.active_round:  # active round already up-to-date
                print('Round already up-to-date, no action')
            else:
                print('Unfreeze activities, rollover completed')
                selling_rouind = active_round_number + 1
                crud.globals.update(db, db_obj=globals, obj_in={
                    'active_round': active_round_number,
                    'selling_round': selling_rouind,
                })  # update round number and unfreeze
                # expire old products
                crud.product.bulk_expire(db, current_round=globals.selling_round)
                crud.globals.update(db, db_obj=globals, obj_in={'is_doing_round_rollover': False})
    finally:
        print(f"Current global state: {jsonable_encoder(crud.globals.get_singleton(db))}")
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
        # "update_globals_task": {
        #     "task": "app.worker.update_globals_task",
        #     "schedule": crontab(day_of_week="sat", hour=18, minute=5),
        # },
        "update_round_rollover": {
            "task": "app.worker.update_round_rollover",
            "schedule": crontab(day_of_week="mon", hour=14, minute=00),
        },
    }
    sender.add_periodic_task(
        settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
        batch_update_payments_task.s(),
        name=f"batch update payments every {settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS} seconds",
    )
    # todo turnkey rollout
