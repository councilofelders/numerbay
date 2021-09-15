from datetime import datetime
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/search", response_model=Dict[str, Union[int, List[schemas.Order]]])
def search_orders(
    db: Session = Depends(deps.get_db),
    role: str = Body(None),
    id: int = Body(None),
    # category_id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = None,
    # term: str = Body(None),
    sort: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    orders = crud.order.search(
        db,
        role=role,
        current_user_id=current_user.id,
        id=id,
        # category_id=category_id,
        skip=skip,
        limit=limit,
        filters=filters,
        # term=term,
        sort=sort,
    )
    return orders


# todo turnkey rollout
# @router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    # Product exists
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Product active
    if not product.is_active:  # todo handle expired api keys
        raise HTTPException(
            status_code=400, detail="This product is not available for sale"
        )

    # Own product
    if product.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot buy your own product")

    # Duplicate order
    selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
    existing_order = crud.order.search(
        db,
        role="buyer",
        current_user_id=current_user.id,
        filters={
            "product": {"in": [product.id]},
            "round_order": {"in": [selling_round]},
        },
    )
    if len(existing_order.get("data", [])) > 0:
        raise HTTPException(
            status_code=400, detail="Order for this product this round already exists"
        )
    if product:
        order_in = schemas.OrderCreate(
            price=product.price,
            currency=product.currency,
            chain=product.chain,
            from_address=current_user.numerai_wallet_address,
            to_address=product.owner.numerai_wallet_address,
            product_id=id,
            date_order=datetime.utcnow(),
            round_order=selling_round,
            state="pending",
        )

        order = crud.order.create_with_buyer(
            db=db, obj_in=order_in, buyer_id=current_user.id
        )
        return order
    return None


# @router.put("/{id}", response_model=schemas.Order)
# def update_order(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     order_in: schemas.OrderUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an order.
#     """
#     order = crud.order.get(db=db, id=id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     if order.owner_id != current_user.id:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     order = crud.order.update(db=db, db_obj=order, obj_in=order_in)
#     return order


# @router.get("/{id}", response_model=schemas.Order)
# def read_order(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get order by ID.
#     """
#     order = crud.order.get(db=db, id=id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order


# @router.delete("/{id}", response_model=schemas.Order)
# def delete_order(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an order.
#     """
#     order = crud.order.get(db=db, id=id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     if order.owner_id != current_user.id:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     order = crud.order.remove(db=db, id=id)
#     return order


# @router.get("/schedule/", response_model=schemas.Msg, status_code=201)
# def schedule(
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Test Celery worker.
#     """
#     result = celery_app.send_task("app.worker.test_celery", args=["123"])
#     return {"msg": result.ready()}