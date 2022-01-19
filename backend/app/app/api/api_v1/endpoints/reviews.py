from datetime import datetime
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/search", response_model=Dict[str, Union[int, List[schemas.Review]]])
def search_reviews(
    db: Session = Depends(deps.get_db),
    id: int = Body(None),
    product_id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = None,
    sort: str = Body(None),
) -> Any:
    """
    Retrieve reviews.
    """
    if skip and skip < 0:
        raise HTTPException(
            status_code=400, detail="Skip must be positive",
        )

    reviews = crud.review.search(
        db,
        id=id,
        product_id=product_id,
        skip=skip,
        limit=limit,
        filters=filters,
        sort=sort,
    )
    return reviews


@router.post("/", response_model=schemas.Review)
def create_review(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int = Body(...),
    rating: int = Body(...),
    text: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new review.
    """
    # Product exists
    product = crud.product.get(db=db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Product active
    if not product.is_active:
        raise HTTPException(status_code=400, detail="This product is not active")

    # Not own product
    if product.owner_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="You cannot review your own product"
        )

    # Mark review verified if bought product
    orders = crud.order.search(
        db,
        role="buyer",
        current_user_id=current_user.id,
        filters={
            "product": {"in": [product.id]},
            "state": {"in": ["pending", "confirmed"]},
        },
    )

    is_verified_order = orders["total"] > 0

    if is_verified_order:
        # Not duplicated review
        existing_reviews = crud.review.search(
            db, product_id=product.id, filters={"user": {"in": [current_user.id]}}
        )
        if existing_reviews["total"] > 0:
            max_round = max(
                [
                    existing_review.round_tournament
                    for existing_review in existing_reviews.get("data", [])
                ]
            )
            orders_since_last_review = [
                order
                for order in orders.get("data", [])
                if order.round_order > max_round
            ]
            if len(orders_since_last_review) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="You already reviewed this product for your most recent order",
                )

        latest_order = max(orders.get("data", []), key=lambda d: d.round_order)
        round_review = latest_order.round_order
    else:
        # Not bought product before
        globals = crud.globals.get_singleton(db=db)
        selling_round = globals.selling_round  # type: ignore
        round_review = selling_round - 1
        existing_reviews = crud.review.search(
            db,
            product_id=product.id,
            filters={
                "user": {"in": [current_user.id]},
                "round_tournament": {"in": [round_review]},
            },
        )
        if existing_reviews["total"] > 0:
            raise HTTPException(
                status_code=400,
                detail="You already reviewed this product for the most recent round",
            )
    if product:
        review_in = schemas.ReviewCreate(
            created_at=datetime.utcnow(),
            round_tournament=round_review,
            rating=rating,
            text=text,
            is_verified_order=is_verified_order,
            reviewer_id=current_user.id,
            product_id=product_id,
        )

        review = crud.review.create(db=db, obj_in=review_in)

        return review
    return None


# @router.put("/{id}", response_model=schemas.Review)
# def update_review(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     review_in: schemas.ReviewUpdate,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update an review.
#     """
#     review = crud.review.get(db=db, id=id)
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     if review.owner_id != current_user.id:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     review = crud.review.update(db=db, db_obj=review, obj_in=review_in)
#     return review


# @router.get("/{id}", response_model=schemas.Review)
# def read_review(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Get review by ID.
#     """
#     review = crud.review.get(db=db, id=id)
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     return review


# @router.delete("/{id}", response_model=schemas.Review)
# def delete_review(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: int,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Delete an review.
#     """
#     review = crud.review.get(db=db, id=id)
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
#     if review.owner_id != current_user.id:
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     review = crud.review.remove(db=db, id=id)
#     return review


# @router.get("/schedule/", response_model=schemas.Msg, status_code=201)
# def schedule(
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Test Celery worker.
#     """
#     result = celery_app.send_task("app.worker.test_celery", args=["123"])
#     return {"msg": result.ready()}
