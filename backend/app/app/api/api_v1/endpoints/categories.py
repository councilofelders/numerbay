from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    slug: str = None,
    skip: int = 0,
    limit: int = None,
) -> Any:
    """
    Retrieve categories.
    """
    if slug:
        categories = crud.category.get_multi_by_slug(
            db, slug=slug, skip=skip, limit=limit
        )
    else:
        categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new category.
    """
    category = crud.category.create(db=db, obj_in=category_in)
    return category


@router.put("/{id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category


@router.get("/{id}", response_model=schemas.Category)
def read_category(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get category by ID.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(db=db, id=id)
    return category
