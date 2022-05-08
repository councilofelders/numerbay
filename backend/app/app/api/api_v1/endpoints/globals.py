""" Globals endpoints """

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps

router = APIRouter()


@router.get("/")
def get_globals(db: Session = Depends(deps.get_db)) -> Any:
    """Get globals"""
    return crud.globals.get_singleton(db)
