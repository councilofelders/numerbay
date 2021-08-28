import sys
from decimal import Decimal

from app.schemas import User
from raven import Client
from celery import group
from celery.schedules import crontab
from celery.canvas import subtask, chord
from celery.result import AsyncResult, allow_join_result

from app import crud, models
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi.encoders import jsonable_encoder


client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def tick(msg: str):
    from datetime import datetime
    print(f'Tick! The time is: {datetime.now()}, arg: {msg}')
    sys.stdout.flush()
    import time
    time.sleep(2)
    return msg


@celery_app.task #(acks_late=True)
def update_model_subtask(user_json):
    db = SessionLocal()
    try:
        return crud.model.update_model(db, user_json)
    finally:
        db.close()


# @celery_app.task(name='FINISH_GROUP') #(acks_late=True)
# def commit_models_subtask(models):
#     print('Callback')
#     print(f'models: {models}')
#     sys.stdout.flush()
#     return True


@celery_app.task #(acks_late=True)
def batch_update_models_task():
    db = SessionLocal()
    try:
        users = crud.user.search(db, filters={'numerai_api_key_public_id': ['any']})['data']
        print(f"total: {len(users)}")
        # result = chord([fetch_model_subtask.s(jsonable_encoder(user), 0) for user in users], commit_models_subtask.s(0)).delay()
        group([update_model_subtask.s(jsonable_encoder(user)) for user in users]).delay()
    finally:
        db.close()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Setup Cron Tasks")
    # sender.add_periodic_task(5.0, batch_update_models_task.s('schedule'), name='add every 5')
    sender.conf.beat_schedule = {
        'test_tick': {
            'task': 'app.worker.tick',
            'schedule': crontab(day_of_week='wed-sun', hour=0, minute=0),
            'args': (['cron test'])
        },
        'batch_update_models': {
            'task': 'app.worker.batch_update_models_task',
            'schedule': crontab(day_of_week='wed-sun', hour=0, minute=0),
        }
    }


