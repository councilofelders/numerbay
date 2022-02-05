import re
import secrets
from datetime import datetime
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.commons import validate_search_params
from app.api.dependencies.polls import (
    generate_voter_id,
    get_voter_weight,
    take_stake_weight_snapshots,
)

router = APIRouter()


@router.post(
    "/search", response_model=Dict[str, Union[int, List[schemas.Poll], List, Dict]]
)
def search_polls(
    db: Session = Depends(deps.get_db),
    id: str = Body(None),  # pylint: disable=W0622
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
) -> Any:
    """
    Retrieve polls.
    """
    validate_search_params(skip=skip)

    polls = crud.poll.search(
        db, id=id, skip=skip, limit=limit, filters=filters, term=term, sort=sort,
    )

    polls_to_return = []
    for poll in polls["data"]:
        poll_to_return = schemas.Poll.from_orm(poll)
        for option in poll_to_return.options:
            if not option.get("selected", False):
                option["selected"] = False
        polls_to_return.append(poll_to_return)

    polls["data"] = polls_to_return
    return polls


@router.post(
    "/search-authenticated",
    response_model=Dict[str, Union[int, List[schemas.Poll], List, Dict]],
)
def search_polls_authenticated(
    db: Session = Depends(deps.get_db),
    id: str = Body(None),  # pylint: disable=W0622
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
    validate_search_params(skip=skip)

    polls = crud.poll.search(
        db, id=id, skip=skip, limit=limit, filters=filters, term=term, sort=sort,
    )

    polls_to_return = []
    for poll in polls["data"]:
        voter_id = generate_voter_id(poll, current_user)
        poll_to_return = schemas.Poll.from_orm(poll)
        user_votes = crud.vote.get_multi_by_poll(db, poll_id=poll.id, voter_id=voter_id)
        if user_votes:
            poll_to_return.has_voted = True

            for v in user_votes:
                poll_to_return.options[v.option]["selected"] = True

        for option in poll_to_return.options:
            if not option.get("selected", False):
                option["selected"] = False

        polls_to_return.append(poll_to_return)

    polls["data"] = polls_to_return
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
    # Numerai API
    numerai.check_user_numerai_api(current_user)

    # id
    if (
        poll_in.id is not None and re.match(r"^[\w-]+$", poll_in.id) is None
    ):  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Invalid id (should only contain "
            "alphabetic characters, numbers, dashes or underscores)",
        )

    if poll_in.id is None or poll_in.id == "":
        poll_in.id = secrets.token_urlsafe(nbytes=8)

    # duplicate ID
    poll = crud.poll.get(db=db, id=poll_in.id)
    if poll:
        raise HTTPException(status_code=400, detail="Poll with this id already exists")

    # blind post determination
    if poll_in.is_blind is False and poll_in.is_stake_predetermined is False:
        raise HTTPException(
            status_code=400,
            detail="Post stake determination is only available for blind polls",
        )

    # valid max_option
    if poll_in.max_options is not None and poll_in.max_options < 1:
        raise HTTPException(
            status_code=400, detail="Max options setting must be at least 1"
        )

    # no max_options for single selection poll
    if poll_in.is_multiple is False and poll_in.max_options is not None:
        raise HTTPException(
            status_code=400,
            detail="Max options setting is not available for single selection polls",
        )

    # valid weight mode
    if poll_in.weight_mode not in [
        "equal",
        "equal_staked",
        "log_numerai_stake",
        "log_numerai_balance",
        "log_balance",
    ]:
        raise HTTPException(status_code=400, detail="Invalid weight mode")

    # todo support numerai balance mode
    if poll_in.weight_mode == "log_numerai_balance":
        raise HTTPException(
            status_code=400,
            detail="log_numerai_balance weight mode is not yet supported",
        )

    # todo support arbitrary balance mode
    if poll_in.weight_mode == "log_balance":
        raise HTTPException(
            status_code=400, detail="log_balance weight mode is not yet supported"
        )

    # valid stake basis round
    if poll_in.stake_basis_round is not None:
        active_round = crud.globals.get_singleton(db=db).active_round  # type: ignore
        # todo dynamic stake_basis_round lower bound based on db
        if poll_in.stake_basis_round > active_round or poll_in.stake_basis_round < 293:
            raise HTTPException(
                status_code=400,
                detail="stake_basis_round must be between 293 and current active round",
            )

    # set pre-determined if not present
    if poll_in.is_stake_predetermined is None:
        poll_in.is_stake_predetermined = True

    # fill stake basis round if not present, if pre-determined
    if poll_in.stake_basis_round is None and poll_in.is_stake_predetermined:
        poll_in.stake_basis_round = crud.globals.get_singleton(  # type: ignore
            db=db
        ).active_round

    # valid min stake
    if poll_in.min_stake is not None and poll_in.min_stake <= 0:
        raise HTTPException(
            status_code=400, detail="Min stake threshold must be positive"
        )

    # valid min rounds
    if poll_in.min_rounds is not None and poll_in.min_rounds not in [0, 13, 52]:
        raise HTTPException(
            status_code=400, detail="Min rounds threshold must be one of 0, 13 or 52"
        )

    # no clipping for non-stake weighted polls
    if poll_in.weight_mode not in [
        "equal_staked",
        "log_numerai_stake",
        "log_numerai_balance",
        "log_balance",
    ] and (poll_in.clip_low is not None or poll_in.clip_high is not None):
        raise HTTPException(
            status_code=400, detail="Clipping is only applicable to NMR weighted modes"
        )

    # valid clipping range
    if poll_in.clip_low is not None and poll_in.clip_low <= 0:
        raise HTTPException(
            status_code=400, detail="Low-side clipping threshold must be positive"
        )

    if poll_in.clip_high is not None and poll_in.clip_high <= 0:
        raise HTTPException(
            status_code=400, detail="High-side clipping threshold must be positive"
        )

    if (
        poll_in.min_stake is not None
        and poll_in.clip_low is not None
        and poll_in.clip_low <= poll_in.min_stake
    ):
        raise HTTPException(
            status_code=400,
            detail="Low-side clipping threshold must be greater than min stake threshold",
        )

    if (
        poll_in.clip_low is not None
        and poll_in.clip_high is not None
        and poll_in.clip_high <= poll_in.clip_low
    ):
        raise HTTPException(
            status_code=400,
            detail="High-side clipping threshold must be greater than low-side clipping threshold",
        )

    # valid number of options
    n_options = len(poll_in.options)
    if n_options < 2 or (
        poll_in.is_multiple
        and (poll_in.max_options is not None)
        and n_options < poll_in.max_options
    ):
        raise HTTPException(status_code=400, detail="Invalid number of options")

    poll_in.date_creation = datetime.utcnow()
    poll_in.owner_id = current_user.id
    poll = crud.poll.create(db=db, obj_in=poll_in)
    return poll


@router.put("/{id}", response_model=schemas.Poll)
def update_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: str,  # pylint: disable=W0622
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
    id: str,  # pylint: disable=W0622
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
    poll = crud.poll.remove(db=db, id=id)  # type: ignore
    return poll


@router.post("/{id}/close", response_model=schemas.Poll)
def close_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: str,  # pylint: disable=W0622
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

    if (
        poll.weight_mode in ["equal_staked", "log_numerai_stake"]
        and not poll.is_stake_predetermined
    ):
        take_stake_weight_snapshots(db, poll)

    poll = crud.poll.update(db=db, db_obj=poll, obj_in={"is_finished": True})
    return poll


@router.post(
    "/{id}", response_model=Dict[str, Union[int, List[schemas.Poll], List, Dict]],
)
def vote(
    *,
    db: Session = Depends(deps.get_db),
    id: str,  # pylint: disable=W0622
    options: List[dict],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Vote for poll.
    """
    date_vote = datetime.utcnow()

    poll = crud.poll.get(db=db, id=id)

    # Poll exists
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    # Poll not finished
    if poll.is_finished or poll.date_finish <= date_vote:
        raise HTTPException(status_code=400, detail="Poll already closed")

    # Valid number of options
    n_options = len(options)
    if (
        n_options < 1
        or (not poll.is_multiple and n_options != 1)
        or (poll.is_multiple and n_options > len(poll.options))  # type: ignore
        or (
            poll.is_multiple
            and (poll.max_options is not None)
            and n_options > poll.max_options
        )
    ):
        raise HTTPException(status_code=400, detail="Invalid number of options")

    # Valid weight
    weight = get_voter_weight(db, poll, current_user)

    # Not voted already
    voter_id = generate_voter_id(poll, current_user)
    existing_votes = crud.vote.get_multi_by_poll(db, poll_id=poll.id, voter_id=voter_id)
    if len(existing_votes) > 0:
        raise HTTPException(status_code=400, detail="You already voted")

    # Valid options
    seen = set()
    for option in options:
        if not isinstance(option["value"], int):
            raise HTTPException(status_code=400, detail="Invalid options")
        if option["value"] >= len(poll.options):  # type: ignore
            raise HTTPException(status_code=400, detail="Invalid options")
        if option["value"] not in seen:
            seen.add(option["value"])
        else:
            raise HTTPException(status_code=400, detail="Duplicated options")

    # Vote
    vote_db_objs = []
    for option in options:
        new_vote_dict = {
            "date_vote": date_vote,
            "option": option["value"],
            "voter_id": voter_id,
            "poll_id": id,
        }

        if poll.is_anonymous is False and poll.weight_mode != "equal":
            new_vote_dict["voter_address"] = current_user.numerai_wallet_address

        new_vote_dict["weight_basis"] = weight
        new_vote = schemas.VoteCreate(**new_vote_dict)

        # crud.vote.create(db, obj_in=new_vote)
        obj_in_data = jsonable_encoder(new_vote)
        db_obj = models.Vote(**obj_in_data)  # type: ignore
        vote_db_objs.append(db_obj)
    db.add_all(vote_db_objs)
    db.commit()

    return search_polls_authenticated(
        db,
        id=id,
        skip=None,  # type: ignore
        limit=None,  # type: ignore
        filters=None,  # type: ignore
        term=None,  # type: ignore
        sort=None,  # type: ignore
        current_user=current_user,
    )
