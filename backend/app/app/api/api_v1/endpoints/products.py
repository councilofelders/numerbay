from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post(
    "/search", response_model=Dict[str, Union[int, List[schemas.Product], List, Dict]]
)
def search_products(
    db: Session = Depends(deps.get_db),
    id: int = Body(None),
    category_id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = Body(None),
    term: str = Body(None),
    sort: str = Body(None),
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.search(
        db,
        id=id,
        category_id=category_id,
        skip=skip,
        limit=limit,
        filters=filters,
        term=term,
        sort=sort,
    )
    return products


@router.get("/my", response_model=List[schemas.Product])
def read_my_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
    products = crud.product.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return products


@router.post("/", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    if product_in.expiration_round is not None:
        selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        if (
            product_in.expiration_round < selling_round
        ):  # deactivate automatically if already expired
            product_in.is_active = False

    category = crud.category.get(db=db, id=product_in.category_id)
    product_in.sku = f"{category.slug}-{product_in.name.lower()}"  # type: ignore
    product = crud.product.get_by_sku(db, sku=product_in.sku)
    if product:
        raise HTTPException(
            status_code=400, detail=f"{product.sku} is already listed.",
        )
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=current_user.id
    )
    return product


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an product.
    """
    if product_in.expiration_round is not None:
        selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        if (
            product_in.expiration_round < selling_round
        ):  # deactivate automatically if already expired
            product_in.is_active = False
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product


@router.get("/{id}", response_model=schemas.Product)
def read_product(*, db: Session = Depends(deps.get_db), id: int,) -> Any:
    """
    Get product by ID.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{id}", response_model=schemas.Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an product.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    product = crud.product.remove(db=db, id=id)
    return product
