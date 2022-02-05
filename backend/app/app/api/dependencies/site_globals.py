from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.models import Globals


def validate_not_during_rollover(db: Session) -> Globals:
    site_globals = crud.globals.get_singleton(db=db)
    if site_globals is None:
        raise HTTPException(
            status_code=400, detail="Failed to read site globals",
        )
    if site_globals.is_doing_round_rollover:
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, "
            "please try again after the round submission deadline",
        )
    return site_globals
