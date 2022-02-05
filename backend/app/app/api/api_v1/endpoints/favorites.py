from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def read_favorites(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve favorites.
    """
    favorites = crud.favorite.get_multi_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    if favorites is not None:
        return [favorite.product for favorite in favorites]
    return []


@router.post("/", response_model=schemas.Favorite)
def create_favorite(
    *,
    db: Session = Depends(deps.get_db),
    favorite_in: schemas.FavoriteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new favorite.
    """
    favorite = crud.favorite.get_by_product(
        db, user_id=current_user.id, product_id=favorite_in.product_id
    )
    if favorite is not None:
        raise HTTPException(
            status_code=400, detail="You already added this product to wishlist"
        )

    favorite = crud.favorite.create(
        db=db,
        obj_in={  # type: ignore
            "user_id": current_user.id,
            "product_id": favorite_in.product_id,
        },
    )
    return favorite


# @router.put("/{id}", response_model=schemas.Favorite)
# def update_favorite(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     favorite_in: schemas.FavoriteUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an favorite.
#     """
#     favorite = crud.favorite.get(db=db, id=id)
#     if not favorite:
#         raise HTTPException(status_code=404, detail="Favorite not found")
#     if not crud.user.is_superuser(current_user) and (favorite.user_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     favorite = crud.favorite.update(db=db, db_obj=favorite, obj_in=favorite_in)
#     return favorite


# @router.get("/{id}", response_model=schemas.Favorite)
# def read_favorite(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get favorite by ID.
#     """
#     favorite = crud.favorite.get(db=db, id=id)
#     if not favorite:
#         raise HTTPException(status_code=404, detail="Favorite not found")
#     if not crud.user.is_superuser(current_user) and (favorite.user_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return favorite


@router.delete("/", response_model=schemas.Favorite)
def delete_favorite(
    *,
    db: Session = Depends(deps.get_db),
    favorite_in: schemas.FavoriteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an favorite.
    """
    favorite = crud.favorite.get_by_product(
        db=db, user_id=current_user.id, product_id=favorite_in.product_id
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    favorite = crud.favorite.remove(db=db, id=favorite.id)
    return favorite
