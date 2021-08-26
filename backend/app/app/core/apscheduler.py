import sys
from datetime import datetime

from fastapi import FastAPI

from app.core.config import settings

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class ScheduleCli(object):

    def __init__(self):
        self._schedule = None

    def init_scheduler(self) -> None:
        print("Starting scheduler")
        job_stores = {
            'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_URI)
        }
        self._schedule = BackgroundScheduler(jobstores=job_stores)
        self._schedule.start()
        print("Scheduler started")
        sys.stdout.flush()

    def __getattr__(self, name):
        return getattr(self._schedule, name)

    def __getitem__(self, name):
        return self._schedule[name]

    def __setitem__(self, name, value):
        self._schedule[name] = value

    def __delitem__(self, name):
        del self._schedule[name]


scheduler: BackgroundScheduler = ScheduleCli()


# @scheduler.scheduled_job('interval', id='test', seconds=5)
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#     sys.stdout.flush()
#
# scheduler.init_scheduler()
# print("Add job")
# scheduler.add_job(tick, 'interval', id='test', seconds=5, replace_existing=True)
# print("Job added")


# def register_init(app: FastAPI) -> None:
#     # @app.on_event("startup")
#     async def init_connect():
#         scheduler.init_scheduler()
#         scheduler.add_job(tick, 'interval', id='test', seconds=5, replace_existing=True)
#
#     # @app.on_event('shutdown')
#     async def shutdown_connect():
#         scheduler.shutdown()


__all__ = ["scheduler"]
