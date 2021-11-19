from datetime import datetime
from decimal import Decimal
import numpy as np
from typing import Any, Dict, List, Union

import secrets

from jose import jwt

from app.core.config import settings
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post(
    "/search", response_model=Dict[str, Union[int, List[schemas.Poll], List, Dict]]
)
def search_polls(
    db: Session = Depends(deps.get_db),
    id: str = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
) -> Any:
    """
    Retrieve polls.
    """
    polls = crud.poll.search(
        db,
        id=id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )
    return polls


@router.post(
    "/search-authenticated", response_model=Dict[str, Union[int, List[schemas.Poll], List, Dict]]
)
def search_polls_authenticated(
    db: Session = Depends(deps.get_db),
    id: str = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve polls (authenticated).
    """
    polls = crud.poll.search(
        db,
        id=id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )

    polls_to_return = []
    for poll in polls['data']:
        voter_id = generate_voter_id(poll, current_user)
        poll_to_return = schemas.Poll.from_orm(poll)
        user_votes = crud.vote.get_multi_by_poll(db, poll_id=poll.id, voter_id=voter_id)
        if user_votes:
            poll_to_return.has_voted = True

            for v in user_votes:
                poll_to_return.options[v.option]['selected'] = True

        for option in poll_to_return.options:
            if not option.get('selected', False):
                option['selected'] = False

        polls_to_return.append(poll_to_return)

    polls['data'] = polls_to_return
    return polls


@router.post("/", response_model=schemas.Poll)
def create_poll(
    *,
    db: Session = Depends(deps.get_db),
    poll_in: schemas.PollCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new poll.
    """
    if poll_in.id is None or poll_in.id == "":
        poll_in.id = secrets.token_urlsafe(nbytes=8)

    # todo validate inputs

    poll_in.date_creation = datetime.utcnow()
    poll_in.owner_id = current_user.id
    poll = crud.poll.create(db=db, obj_in=poll_in)
    return poll


@router.put("/{id}", response_model=schemas.Poll)
def update_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    poll_in: schemas.PollUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an poll.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if poll.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.update(db=db, db_obj=poll, obj_in=poll_in)
    return poll


# @router.get("/{id}", response_model=schemas.Poll)
# def read_poll(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     # current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get poll by ID.
#     """
#     poll = crud.poll.get(db=db, id=id)
#     if not poll:
#         raise HTTPException(status_code=404, detail="Poll not found")
#     # if not crud.user.is_superuser(current_user) and (poll.owner_id != current_user.id):
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     return poll


@router.delete("/{id}", response_model=schemas.Poll)
def delete_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an poll.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if poll.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.remove(db=db, id=id)
    return poll

def generate_voter_id(poll, user) -> str:
    if poll.is_anonymous:
        # todo other wallet support
        to_encode = {"poll_id": poll.id, "voter_address": user.numerai_wallet_address}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt
    else:
        return str(user.id)


def get_voter_weight(db: Session, poll, user) -> Decimal:
    if poll.weight_mode == "equal":
        weight = 1
    elif poll.weight_mode == "log_numerai_stake":
        user_models_snapshots = db.query(models.Model).join(models.StakeSnapshot,
                                                            models.Model.id == models.StakeSnapshot.model_id).filter(
            models.Model.owner_id == user.id).all()
        user_nmr_staked = sum([model_snapshot.nmr_staked for model_snapshot in user_models_snapshots])
        weight = Decimal(user_nmr_staked).ln()
    elif poll.weight_mode == "log_numerai_balance":
        raise HTTPException(status_code=400, detail="Weight mode not yet supported")
    elif poll.weight_mode == "log_balance":
        raise HTTPException(status_code=400, detail="Weight mode not yet supported")
    else:
        raise HTTPException(status_code=400, detail="Invalid weight mode")

    return weight

@router.post("/{id}")
def vote(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    options: List[dict],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Vote for poll.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    # todo validate input

    date_vote = datetime.utcnow()

    for option in options:
        new_vote_dict = {
            "date_vote": date_vote,
            "option": option["value"],
            "voter_id": generate_voter_id(poll, current_user),
            "poll_id": id
        }

        new_vote_dict['weight_basis'] = get_voter_weight(db, poll, current_user)




        new_vote = schemas.VoteCreate(**new_vote_dict)
        crud.vote.create(db, obj_in=new_vote)
    return search_polls_authenticated(db, id=id, skip=None,
    limit=None,
    filters=None,
    term=None,
    sort=None, current_user=current_user)
