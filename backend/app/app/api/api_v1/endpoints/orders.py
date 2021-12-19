from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.coupons import calculate_option_price
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import send_new_order_email

router = APIRouter()


@router.post("/search", response_model=Dict[str, Union[int, List[schemas.Order]]])
def search_orders(
    db: Session = Depends(deps.get_db),
    role: str = Body(None),
    id: int = Body(None),
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = None,
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
        skip=skip,
        limit=limit,
        filters=filters,
        sort=sort,
    )
    return orders


@router.post("/", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int = Body(...),
    option_id: int = Body(...),
    quantity: int = Body(...),
    submit_model_id: str = Body(None),
    coupon: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    # record time immediately to prevent timing issue
    # todo resolve timing issue
    date_order = datetime.utcnow() - timedelta(minutes=1)

    # Product exists
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_option = crud.product_option.get(db=db, id=option_id)
    if not product_option:
        raise HTTPException(status_code=404, detail="Product option not found")

    if product_option.product_id != product.id:
        raise HTTPException(status_code=400, detail="Invalid product option")

    # Product Option on-platform
    if not product_option.is_on_platform:
        raise HTTPException(
            status_code=400, detail="This product option is not on-platform"
        )

    # Quantity
    if quantity < 1:
        raise HTTPException(
            status_code=400, detail="Order quantity must be positive",
        )

    total_quantity = (
        product_option.quantity * quantity
        if product_option.quantity is not None
        else quantity
    )
    if not product.category.is_per_round and total_quantity > 1:
        raise HTTPException(
            status_code=400,
            detail="This product is not per-round, order quantity must be 1",
        )

    # Product active
    if not product.is_active:  # todo handle expired api keys
        raise HTTPException(
            status_code=400, detail="This product is not available for sale"
        )

    # Own product
    if product.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot buy your own product")

    # Addresses
    from_address = current_user.numerai_wallet_address
    to_address = (
        product_option.wallet
        if product_option.wallet
        else product.owner.numerai_wallet_address
    )

    if not to_address or not from_address:
        raise HTTPException(status_code=400, detail="Invalid buyer / seller address")

    # Own address
    if from_address == to_address:
        raise HTTPException(status_code=400, detail="You cannot buy your own product")

    # Duplicate order
    globals = crud.globals.get_singleton(db=db)
    selling_round = globals.selling_round  # type: ignore
    existing_order = crud.order.search(
        db,
        role="buyer",
        current_user_id=current_user.id,
        filters={
            "product": {"in": [product.id]},
            "round_order": {"in": [selling_round]},
            "state": {"in": ["pending", "confirmed"]},
        },
    )
    if len(existing_order.get("data", [])) > 0:
        raise HTTPException(
            status_code=400, detail="Order for this product this round already exists"
        )

    # Not during round rollover
    if globals.is_doing_round_rollover:  # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Round rollover in progress, please try again after the round submission deadline",
        )

    # todo test
    # Compulsory submit model for non-file modes
    if product_option.mode != "file" and submit_model_id is None:
        raise HTTPException(
            status_code=400,
            detail="Specifying Numerai model ID for submission is required for this product option",
        )

    # Numerai API
    numerai.check_user_numerai_api(current_user)

    # Numerai api permissions
    if product_option.mode != "file" or (
        submit_model_id is not None
    ):  # if stake modes or file mode with submit_model_id
        # check buyer api permissions
        if (
            product_option.mode == "stake_with_limit"
            and not current_user.numerai_api_key_can_stake
        ):
            raise HTTPException(
                status_code=403,
                detail="Numerai API Key does not have permission to stake",
            )
        if not current_user.numerai_api_key_can_upload_submission:
            raise HTTPException(
                status_code=403,
                detail="Numerai API Key does not have permission to upload submissions",
            )

    # Own submit model id
    submit_models = [
        model
        for model in current_user.models  # type: ignore
        if model.tournament == product.model.tournament and model.id == submit_model_id
    ]
    if submit_model_id is not None and len(submit_models) == 0:
        raise HTTPException(
            status_code=403, detail="Invalid Numerai model ID for submission"
        )

    if product:
        # todo test coupon
        coupon_obj = crud.coupon.get_by_code(db, code=coupon)
        product_option_obj = schemas.ProductOption.from_orm(product_option)
        product_option_obj = calculate_option_price(
            product_option_obj, coupon=coupon, coupon_obj=coupon_obj, qty=quantity
        )

        order_in = schemas.OrderCreate(
            quantity=total_quantity,
            price=product_option_obj.special_price
            if product_option_obj.applied_coupon
            else product_option_obj.price,
            currency=product_option.currency,
            mode=product_option.mode,
            stake_limit=product_option.stake_limit,
            submit_model_id=submit_model_id,
            submit_model_name=submit_models[0].name
            if (submit_model_id and len(submit_models) > 0)
            else None,
            chain=product_option.chain,
            from_address=from_address,
            to_address=to_address,
            product_id=id,
            date_order=date_order,
            round_order=selling_round,
            state="pending",
            applied_coupon_id=coupon_obj.id  # type: ignore
            if product_option_obj.applied_coupon
            else None,
            coupon=product_option_obj.coupon,
            coupon_specs=product_option_obj.coupon_specs,
        )

        order = crud.order.create_with_buyer(
            db=db, obj_in=order_in, buyer_id=current_user.id
        )

        if settings.EMAILS_ENABLED:
            # email buyer
            if current_user.email:
                send_new_order_email(
                    email_to=current_user.email,
                    username=current_user.username,
                    timeout=settings.PENDING_ORDER_EXPIRE_MINUTES,
                    round_order=order.round_order,
                    date_order=order.date_order,
                    product=product.sku,
                    from_address=order.from_address,  # type: ignore
                    to_address=order.to_address,  # type: ignore
                    amount=order.price,
                    currency=order.currency,  # type: ignore
                )
        return order
    return None


@router.post("/{order_id}/submit-artifact/{artifact_id}")
def submit_artifact(
    *,
    order_id: int,
    artifact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.buyer_id != current_user.id and order.product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "confirmed":
        raise HTTPException(status_code=403, detail="Order not confirmed")
    if not order.submit_model_id:
        raise HTTPException(
            status_code=400, detail="Order does not have a model ID to submit to"
        )
    if not order.buyer.numerai_api_key_can_upload_submission:
        raise HTTPException(
            status_code=403,
            detail="Buyer's Numerai API Key does not have permission to upload submissions",
        )
    if order.submit_state == "queued":
        raise HTTPException(
            status_code=400, detail="Submission for this order is already queued"
        )

    active_round = crud.globals.get_singleton(db=db).active_round  # type: ignore

    artfact = crud.artifact.get(db, id=artifact_id)
    if not artfact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    if not artfact.object_name:
        raise HTTPException(
            status_code=400,
            detail="Automated submission is not supported for external artifact URL",
        )
    if artfact.round_tournament != active_round:
        raise HTTPException(
            status_code=400, detail=f"Round {artfact.round_tournament} is not active"
        )
    if artfact.product_id != order.product_id:
        raise HTTPException(status_code=400, detail="Invalid artifact")

    celery_app.send_task(
        "app.worker.upload_numerai_artifact_task",
        kwargs=dict(
            order_id=order.id,
            object_name=artfact.object_name,
            model_id=order.submit_model_id,
            numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,
            numerai_api_key_secret=order.buyer.numerai_api_key_secret,
            tournament=order.product.model.tournament,
            version=1,
        ),
    )
    crud.order.update(db, db_obj=order, obj_in={"submit_state": "queued"})
    return {"msg": "success!"}


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
