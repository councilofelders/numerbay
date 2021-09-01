from typing import Any

from fastapi import APIRouter, Depends

from app import crud
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/")
def get_globals() -> Any:
    return crud.globals.get_singleton()
