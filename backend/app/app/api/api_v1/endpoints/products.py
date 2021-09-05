from decimal import Decimal
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


def validate_product(
    db: Session, product_in: Union[schemas.ProductCreate, schemas.ProductUpdate]
) -> Union[schemas.ProductCreate, schemas.ProductUpdate]:
    # Positive price
    if product_in.price is not None:
        if product_in.price <= 0:
            raise HTTPException(
                status_code=400, detail="Price must be positive",
            )

    # Positive expiration round
    if product_in.expiration_round is not None:
        if product_in.expiration_round <= 0:
            raise HTTPException(
                status_code=400, detail="Expiration round must be a positive integer",
            )

        # deactivate automatically if already expired
        selling_round = crud.globals.get_singleton(db).selling_round  # type: ignore
        if product_in.expiration_round < selling_round:
            product_in.is_active = False

    # Make currency upper case
    if product_in.currency is not None:
        product_in.currency = product_in.currency.upper()

    if product_in.is_on_platform is not None:
        if product_in.is_on_platform:
            # On-platform currency type
            if product_in.currency is not None and product_in.currency not in ["NMR"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"{product_in.currency} is not supported for on-platform listing",
                )

            # On-platform decimal check
            if product_in.price is not None:
                precision = Decimal(product_in.price).as_tuple().exponent
                if precision < -4:
                    raise HTTPException(
                        status_code=400,
                        detail=f"On-platform listing price must not exceed {4} decimal places",
                    )

            # On-platform chain type
            if product_in.chain is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Specifying chain is not yet supported for on-platform listing",
                )
        else:
            # Off-platform currency type
            if product_in.currency is not None and product_in.currency not in ["USD"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"{product_in.currency} is not supported for off-platform listing",
                )

            # Off-platform decimal check
            if product_in.price is not None:
                precision = Decimal(product_in.price).as_tuple().exponent
                if precision < -2:
                    raise HTTPException(
                        status_code=400,
                        detail=f"On-platform listing price must not exceed {2} decimal places",
                    )

            # Off-platform chain type
            if product_in.chain is not None:
                raise HTTPException(
                    status_code=400,
                    detail="Specifying chain is not supported for off-platform listing",
                )

    # Avatar url scheme
    if product_in.avatar and not product_in.avatar.startswith("https"):
        raise HTTPException(
            status_code=400, detail="Avatar image must be a HTTPS URL",
        )

    return product_in


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
    # todo turnkey rollout
    if product_in.is_on_platform is not None and product_in.is_on_platform:
        raise HTTPException(
            status_code=400, detail="On-platform listing is not yet available",
        )

    product_in = validate_product(db, product_in)  # type: ignore

    # Category
    category = crud.category.get(db=db, id=product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Leaf category
    child_categories_count = (
        db.query(models.Category)
        .filter(models.Category.parent_id == category.id)
        .count()
    )
    if child_categories_count > 0:
        raise HTTPException(
            status_code=400, detail="Category must be a leaf category",
        )

    # Existing listing
    sku = f"{category.slug}-{product_in.name.lower()}"  # type: ignore
    product = crud.product.get_by_sku(db, sku=sku)
    if product:
        raise HTTPException(
            status_code=400, detail=f"{product.sku} is already listed",
        )

    # Model ownership
    model = crud.model.get_by_name(db, name=product_in.name)
    if not model:
        raise HTTPException(
            status_code=404, detail="Model not found",
        )
    if model.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this model",
        )

    # Create product
    product = crud.product.create_with_owner(
        db=db, obj_in=product_in, owner_id=current_user.id, sku=sku, model_id=model.id
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
    # todo turnkey rollout
    if product_in.is_on_platform is not None and product_in.is_on_platform:
        raise HTTPException(
            status_code=400, detail="On-platform listing is not yet available",
        )

    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_in = validate_product(db, product_in)  # type: ignore

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

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
