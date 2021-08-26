import sys

from app.core.config import settings
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler



# @app.on_event('startup')
# def init_scheduler():
print("Starting scheduler")
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_URI)
}

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.configure(jobstores=jobstores)

scheduler.start()
print("Scheduler started")
sys.stdout.flush()
