import datetime
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.poll import PollCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_poll(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    is_multiple: bool = False,
    weight_mode: Optional[str] = "equal",
) -> models.Poll:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    poll_id = "zzz" + random_lower_string()

    description = random_lower_string()

    poll_in = PollCreate(
        id=poll_id,
        topic=poll_id,
        description=description,
        date_creation=datetime.datetime.utcnow(),
        date_finish=datetime.date(2032, 12, 31),
        is_multiple=is_multiple,
        max_options=2,
        is_anonymous=True,
        is_blind=True,
        weight_mode=weight_mode,
        stake_basis_round=293,
        owner_id=owner_id,
        options=[
            {"value": 0, "text": "Python"},
            {"value": 1, "text": "R"},
            {"value": 2, "text": "Java"},
        ],
    )

    poll = crud.poll.create(
        db=db,
        obj_in=poll_in,
    )

    return poll


@contextmanager
def get_random_poll(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    is_multiple: bool = False,
    weight_mode: Optional[str] = "equal",
) -> Generator:
    poll = create_random_poll(
        db, owner_id=owner_id, is_multiple=is_multiple, weight_mode=weight_mode
    )
    try:
        yield poll
    finally:
        owner_id_tmp = poll.owner_id
        crud.poll.remove(db, id=poll.id)  # type: ignore
        if owner_id is None:
            crud.user.remove(db, id=owner_id_tmp)  # type: ignore
