import datetime
from typing import Optional

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
    id = "zzz" + random_lower_string()

    description = random_lower_string()

    poll_in = PollCreate(
        id=id,
        topic=id,
        description=description,
        date_creation=datetime.datetime.utcnow(),
        date_finish=datetime.date(2032, 12, 31),
        is_multiple=is_multiple,
        max_options=2,
        is_anonymous=True,
        is_blind=True,
        weight_mode=weight_mode,
        owner_id=owner_id,
        options=[
            {"value": 0, "text": "Python"},
            {"value": 1, "text": "R"},
            {"value": 2, "text": "Java"},
        ],
    )

    poll = crud.poll.create(db=db, obj_in=poll_in,)

    return poll
