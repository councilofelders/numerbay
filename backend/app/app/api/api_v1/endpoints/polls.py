from typing import Any, Dict, List, Union

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
    products = crud.poll.search(
        db,
        id=id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )
    return products


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
    poll = crud.poll.create_with_owner(db=db, obj_in=poll_in, owner_id=current_user.id)
    return poll


@router.put("/{id}", response_model=schemas.Poll)
def update_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    poll_in: schemas.PollUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an poll.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not crud.user.is_superuser(current_user) and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.update(db=db, db_obj=poll, obj_in=poll_in)
    return poll


@router.get("/{id}", response_model=schemas.Poll)
def read_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get poll by ID.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    # if not crud.user.is_superuser(current_user) and (poll.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return poll


@router.delete("/{id}", response_model=schemas.Poll)
def delete_poll(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an poll.
    """
    poll = crud.poll.get(db=db, id=id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    if not crud.user.is_superuser(current_user) and (poll.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    poll = crud.poll.remove(db=db, id=id)
    return poll
