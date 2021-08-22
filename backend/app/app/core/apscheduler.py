from app.core.config import settings
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler



# @app.on_event('startup')
# def init_scheduler():
print("Starting scheduler")
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.SQLALCHEMY_DATABASE_URI)
}
# executors = {
#     'default': {'type': 'threadpool', 'max_workers': 20},
#     'processpool': ProcessPoolExecutor(max_workers=5)
# }
scheduler = AsyncIOScheduler()
scheduler.configure(jobstores=jobstores)  # , executors=executors

scheduler.start()
print("Scheduler started")
