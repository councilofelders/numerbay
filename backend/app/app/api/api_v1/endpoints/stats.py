""" Stats endpoints """

from typing import Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import crud
from app.api import deps

router = APIRouter()


@router.get("/")
def get_stats(response: Response, db: Session = Depends(deps.get_db)) -> Any:
    """Get stats"""
    response.headers["Cache-Control"] = "public, max-age=300"
    return crud.stats.get_singleton(db)
