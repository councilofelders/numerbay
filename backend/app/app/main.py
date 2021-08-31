from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# register_init(app)


# scheduler.init_scheduler()

# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#     sys.stdout.flush()


# if __name__ == '__main__':
#     print("Add job")
#     sys.stdout.flush()
#     scheduler.add_job(tick, 'interval', id='test', seconds=5, replace_existing=True)
#     print("Job added")
#     sys.stdout.flush()

# @app.get('/test-sh')
# def test():
#     print("Add job")
#     sys.stdout.flush()
#     scheduler.add_job(tick, 'interval', id='test', seconds=5, replace_existing=True)
#     print("Job added")
#     sys.stdout.flush()