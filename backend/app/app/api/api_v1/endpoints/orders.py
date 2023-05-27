""" Orders endpoints """
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from web3 import Web3

from app import crud, models, schemas
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.commons import validate_search_params
from app.api.dependencies.coupons import calculate_option_price
from app.api.dependencies.orders import (
    any_weekday_round,
    on_order_confirmed,
    send_order_canceled_emails,
    send_order_refund_request_emails,
    send_order_upload_reminder_emails,
    valid_rounds,
    validate_existing_order,
)
from app.api.dependencies.products import (
    validate_existing_product,
    validate_existing_product_option,
)
from app.api.dependencies.site_globals import validate_not_during_rollover
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import send_new_order_email

router = APIRouter()


@router.post("/search", response_model=Dict[str, Union[int, List[schemas.Order]]])
def search_orders(  # pylint: disable=too-many-arguments
    db: Session = Depends(deps.get_db),
    role: str = Body(None),
    id: int = Body(None),  # pylint: disable=W0622
    skip: int = Body(None),
    limit: int = Body(None),
    filters: Dict = None,
    sort: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    validate_search_params(skip=skip)

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
def create_order(  # pylint: disable=too-many-locals,too-many-branches
    *,
    db: Session = Depends(deps.get_db),
    id: int = Body(...),  # pylint: disable=W0622
    option_id: int = Body(...),
    rounds: List[int] = Body(...),
    submit_model_id: str = Body(None),
    coupon: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    # record time immediately to prevent timing issue
    date_order = datetime.utcnow() - timedelta(minutes=1)

    # Product exists
    product = validate_existing_product(db, id)
    product_option = validate_existing_product_option(db, option_id)

    if product_option.product_id != product.id:
        raise HTTPException(status_code=400, detail="Invalid product option")

    # Encryption key check
    if (
        product.use_encryption
        and current_user.public_key is None
        and current_user.public_key_v2 is None
    ):
        raise HTTPException(
            status_code=400, detail="This product requires encryption key"
        )

    # Product Option on-platform
    if not product_option.is_on_platform:
        raise HTTPException(
            status_code=400, detail="This product option is not on-platform"
        )

    # Quantity
    total_quantity = len(rounds)
    if total_quantity < 1:
        raise HTTPException(
            status_code=400,
            detail="Order quantity must be positive",
        )

    # total_quantity = (
    #     product_option.quantity * quantity
    #     if product_option.quantity is not None
    #     else quantity
    # )
    if not product.category.is_per_round and total_quantity > 1:
        raise HTTPException(
            status_code=400,
            detail="This product is not per-round, order quantity must be 1",
        )

    # Product active
    if not product.is_active:
        raise HTTPException(
            status_code=400, detail="This product is not available for sale"
        )

    # Check daily product
    if any_weekday_round(rounds) and not product.is_daily:
        raise HTTPException(
            status_code=400, detail="This product is not available for weekday sale"
        )

    # Check invalid rounds
    site_globals = validate_not_during_rollover(db)
    selling_round = site_globals.selling_round  # type: ignore
    if (
        not valid_rounds(
            rounds,
            selling_round=selling_round,
            max_round_offset=settings.MAX_ROUND_OFFSET,
            round_lock=product.round_lock,
        )
        and not current_user.is_superuser
    ):
        raise HTTPException(status_code=400, detail="Invalid tournament round(s)")

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

    # Other pending order
    pending_orders = crud.order.search(
        db,
        role="buyer",
        current_user_id=current_user.id,
        filters={
            "state": {"in": ["pending"]},
        },
    )
    if len(pending_orders.get("data", [])) > 0 and not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="Please pay for or cancel your pending order before making a new order",
        )

    # Duplicate order
    existing_order = crud.order.search(
        db,
        role="buyer",
        current_user_id=current_user.id,
        filters={
            "product": {"in": [product.id]},
            "round_order": {"in": rounds},
            "state": {"in": ["pending", "confirmed"]},
        },
    )
    if len(existing_order.get("data", [])) > 0:
        raise HTTPException(
            status_code=400, detail="Order for this product this round already exists"
        )

    # Compulsory submit model for non-file modes
    if product_option.mode != "file" and submit_model_id is None:
        raise HTTPException(
            status_code=400,
            detail="Specifying Numerai model ID for submission is required for this product option",
        )

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

    # Numerai API
    numerai.check_user_numerai_api(current_user)

    # Own submit model id
    submit_models = [
        model
        for model in current_user.models  # type: ignore
        if product.model
        and model.tournament == product.model.tournament
        and model.id == submit_model_id
    ]
    if submit_model_id is not None and len(submit_models) == 0:
        # Attempt Numerai API sync
        user_json = jsonable_encoder(current_user)
        numerai.sync_user_numerai_api(db, user_json)

        # Try to resolve model again
        submit_models = [
            model
            for model in current_user.models  # type: ignore
            if model.tournament == product.model.tournament
            and model.id == submit_model_id
        ]

        # Fails again, raise error
        if len(submit_models) == 0:
            raise HTTPException(
                status_code=403, detail="Invalid Numerai model ID for submission"
            )

    if product:
        coupon_obj = crud.coupon.get_by_code(db, code=coupon)
        product_option_obj = schemas.ProductOption.from_orm(product_option)
        product_option_obj = calculate_option_price(
            db,
            product_option_obj,
            coupon=coupon,
            coupon_obj=coupon_obj,
            qty=total_quantity,
            user=current_user,
        )

        rounds_sorted = sorted(rounds)
        final_price = (
            product_option_obj.special_price
            if product_option_obj.applied_coupon
            else product_option_obj.price
        )

        # check min price # todo add test
        if final_price < 1:  # type: ignore
            raise HTTPException(
                status_code=400,
                detail="Total amounts paid must be greater than 1 NMR",
            )

        order_in = schemas.OrderCreate(
            rounds=rounds_sorted,
            price=final_price,
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
            buyer_public_key=(
                current_user.public_key
                if not current_user.public_key_v2
                else current_user.public_key_v2
            )
            if product.use_encryption
            else None,  # validate buyer key exists
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
    """Submit artifact"""
    order = validate_existing_order(db, order_id)

    if (
        order.buyer_id != current_user.id  # pylint: disable=consider-using-in
        and order.product.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "confirmed":
        raise HTTPException(status_code=400, detail="Order not confirmed")
    if not order.submit_model_id:
        raise HTTPException(
            status_code=400, detail="Order does not have a model ID to submit to"
        )
    if not order.buyer.numerai_api_key_can_upload_submission:
        raise HTTPException(
            status_code=403,
            detail="Buyer's Numerai API Key does not have permission to upload submissions",
        )
    # Disable queue check to always redo queuing
    # if order.submit_state == "queued":
    #     raise HTTPException(
    #         status_code=400, detail="Submission for this order is already queued"
    #     )

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


@router.post("/{order_id}/submission-model")
def update_submission_model(
    *,
    order_id: int,
    model_id: str = Body(None, embed=True),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update auto-submission model"""
    order = validate_existing_order(db, order_id)

    if (
        order.buyer_id != current_user.id  # pylint: disable=consider-using-in
        and order.product.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "confirmed":
        raise HTTPException(status_code=400, detail="Order not confirmed")
    if order.mode == "stake_with_limit":
        raise HTTPException(
            status_code=400,
            detail="Order with stake limit cannot change submission model",
        )

    if model_id is None or model_id == "":
        order = crud.order.update(
            db,
            db_obj=order,
            obj_in={"submit_model_id": None, "submit_model_name": None},
        )
        return order

    model = crud.model.get(db, id=model_id)
    if model is None:
        raise HTTPException(status_code=400, detail="Invalid model ID")
    if model.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Invalid model ownership")
    if model.tournament != order.product.category.tournament:
        raise HTTPException(status_code=400, detail="Invalid model tournament")

    order = crud.order.update(
        db,
        db_obj=order,
        obj_in={"submit_model_id": model.id, "submit_model_name": model.name},
    )
    return order


@router.post("/{order_id}/payment/{transaction_hash}")
def validate_payment(
    *,
    order_id: int,
    transaction_hash: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Validate payment"""
    order = validate_existing_order(db, order_id)
    if (
        order.buyer_id != current_user.id  # pylint: disable=consider-using-in
        and order.product.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "pending":
        raise HTTPException(status_code=400, detail="Order not pending")

    # todo validate transaction_hash
    abi = [
        {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "from", "type": "address"},
                {"indexed": True, "name": "to", "type": "address"},
                {"indexed": False, "name": "value", "type": "uint256"},
            ],
            "name": "Transfer",
            "type": "event",
        },
    ]

    infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_PROJECT_ID}"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    contract = web3.eth.contract(
        address=Web3.toChecksumAddress(settings.NMR_CONTRACT_ADDRESS), abi=abi
    )

    tx_receipt = web3.eth.getTransactionReceipt(transaction_hash)
    if tx_receipt:
        transfer_event = contract.events.Transfer().processReceipt(tx_receipt)
        transaction_timestamp = datetime.utcfromtimestamp(
            web3.eth.getBlock(transfer_event[0]["blockNumber"])["timestamp"]
        )

        # time check
        if transaction_timestamp < order.date_order:
            raise HTTPException(status_code=400, detail="Invalid transaction timestamp")

        transaction_from = transfer_event[0]["args"]["from"].lower()
        transaction_to = transfer_event[0]["args"]["to"].lower()
        if transaction_to != order.to_address.lower():  # type: ignore
            raise HTTPException(
                status_code=400, detail="Transaction recipient mismatch"
            )
        if (
            transaction_from != order.from_address
            and transaction_from != current_user.public_address
        ):
            raise HTTPException(status_code=400, detail="Transaction sender mismatch")
        transaction_amount = web3.fromWei(transfer_event[0]["args"]["value"], "ether")
        if transaction_amount != order.price:
            raise HTTPException(status_code=400, detail="Transaction amount mismatch")

        # existing match check
        existing_match = (
            db.query(models.Order)
            .filter(models.Order.transaction_hash == transaction_hash)
            .first()
        )
        if existing_match is not None:
            raise HTTPException(status_code=400, detail="Duplicated transaction hash")

        on_order_confirmed(db, order, transaction_hash)

        return order

    raise HTTPException(status_code=400, detail="Invalid transaction hash")


@router.delete("/{order_id}", response_model=schemas.Order)
def cancel_order(
    *,
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Cancel order"""
    order = validate_existing_order(db, order_id)
    if order.buyer_id != current_user.id:  # pylint: disable=consider-using-in
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "pending":
        raise HTTPException(status_code=400, detail="Order not pending")

    order = crud.order.update(db, db_obj=order, obj_in={"state": "expired"})
    send_order_canceled_emails(order)
    return order


@router.post("/{order_id}/upload-reminder")
def send_upload_reminder(
    *,
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Send upload reminder to seller"""
    order = validate_existing_order(db, order_id)

    if order.buyer_id != current_user.id:  # pylint: disable=consider-using-in
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "confirmed":
        raise HTTPException(status_code=400, detail="Order not confirmed")

    datetime_now = datetime.utcnow()
    if order.last_reminder_date is not None and (
        datetime_now - order.last_reminder_date
    ) < timedelta(minutes=settings.ORDER_UPLOAD_REMINDER_TIMEOUT_MINUTES):
        raise HTTPException(
            status_code=400,
            detail=f"Please wait for {settings.ORDER_UPLOAD_REMINDER_TIMEOUT_MINUTES} "
            f"minutes before sending another reminder",
        )

    send_order_upload_reminder_emails(order)

    crud.order.update(db, db_obj=order, obj_in={"last_reminder_date": datetime_now})
    return {"msg": "success!"}


@router.post("/{order_id}/refund-request")
def send_refund_request(
    *,
    order_id: int,
    wallet: str = Body(...),
    contact: str = Body(None),
    message: str = Body(None),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Send refund request to seller"""
    order = validate_existing_order(db, order_id)

    if order.buyer_id != current_user.id:  # pylint: disable=consider-using-in
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if order.state != "confirmed":
        raise HTTPException(status_code=400, detail="Order not confirmed")

    datetime_now = datetime.utcnow()
    if order.last_reminder_date is not None and (
        datetime_now - order.last_reminder_date
    ) < timedelta(minutes=settings.ORDER_UPLOAD_REMINDER_TIMEOUT_MINUTES):
        raise HTTPException(
            status_code=400,
            detail=f"Please wait for {settings.ORDER_UPLOAD_REMINDER_TIMEOUT_MINUTES} "
            f"minutes before sending another request",
        )

    # cleaning strings
    TAG_RE = re.compile(r"<[^>]+>")
    wallet = TAG_RE.sub("", wallet)
    contact = TAG_RE.sub("", contact)
    message = TAG_RE.sub("", message)

    send_order_refund_request_emails(
        order, wallet=wallet, contact=contact, message=message
    )

    crud.order.update(db, db_obj=order, obj_in={"last_reminder_date": datetime_now})
    return {"msg": "success!"}
