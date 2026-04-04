""" Dependencies for orders endpoints """

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Dict, List, Optional

import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import lazyload

from app import crud, models
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.coupons import (
    create_coupon_for_order,
    send_new_coupon_email_for_coupon,
)
from app.core.async_tasks import (
    enqueue_trigger_webhook_for_product,
    enqueue_update_payment,
    enqueue_upload_numerai_artifact,
)
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import (
    send_failed_autosubmit_buyer_email,
    send_failed_autosubmit_seller_email,
    send_new_confirmed_sale_email,
    send_order_artifact_upload_reminder_email,
    send_order_canceled_email,
    send_order_confirmed_email,
    send_order_expired_email,
    send_order_refund_request_email,
)

ORDER_CONFIRMATION_SIDE_EFFECTS_KEY = "confirmation_side_effects"
ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY = "upload_enqueued"
ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY = "webhook_enqueued"
ORDER_CONFIRMATION_EMAILS_SENT_KEY = "emails_sent"


def validate_existing_order(db: Session, order_id: int) -> models.Order:
    """Validate existing order"""
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_order_round_numbers(round_order: int, quantity: int) -> List[int]:
    return list(range(round_order, round_order + quantity))


def any_weekday_round(rounds_numbers: List[int]) -> bool:
    for round_number in rounds_numbers:
        if round_number <= 339:
            continue
        if ((round_number - 339) % 5) != 0:
            return True
    return False


def valid_rounds(
    rounds_numbers: List[int],
    selling_round: int,
    max_round_offset: int,
    round_lock: Optional[int] = None,
) -> bool:
    for round_number in rounds_numbers:
        if (
            round_number < selling_round
            or round_number > selling_round + max_round_offset
        ):
            return False

        if round_lock and round_number <= round_lock:
            return False
    return True


def match_transaction_for_order(db: Session, order_obj: models.Order) -> Optional[str]:
    """Match transaction for order"""
    matched_transaction = None
    try:
        numerai_wallet_transactions = numerai.get_numerai_wallet_transactions(
            public_id=order_obj.buyer.numerai_api_key_public_id,  # type: ignore
            secret_key=order_obj.buyer.numerai_api_key_secret,  # type: ignore
        )
        for transaction in numerai_wallet_transactions:
            time = pd.to_datetime(transaction["time"]).tz_localize(None).to_pydatetime()
            if time < order_obj.date_order:
                continue
            if transaction["to"].lower() == order_obj.to_address.lower():
                print(
                    f"Transaction match for order {order_obj.id} "
                    f"[{order_obj.buyer.username}->{order_obj.product.name}], "
                    f"{transaction['amount']} {order_obj.currency} / "
                    f"{order_obj.price} {order_obj.currency}, status: {transaction['status']}"
                )

                # existing match
                existing_match = (
                    db.query(models.Order)
                    .filter(models.Order.transaction_hash == transaction["txHash"])
                    .first()
                )
                if existing_match is not None:
                    print(
                        f"Transaction {transaction['txHash']} already matched, skipping... "
                    )
                    continue

                # Confirmed
                if (
                    Decimal(transaction["amount"]) >= Decimal(order_obj.price)
                    and transaction["status"] == "confirmed"
                ):
                    matched_transaction = transaction["txHash"]
                    break
    except Exception:  # pylint: disable=broad-except
        pass
    return matched_transaction


def on_order_confirmed(
    db: Session, order_obj: models.Order, transaction: Optional[str] = None
) -> None:
    """On order confirmed"""
    coupon_obj = None
    if order_obj.state != "confirmed":
        order_obj.transaction_hash = transaction
        order_obj.state = "confirmed"
        db.add(order_obj)
        db.flush()

        coupon_obj = create_coupon_for_order(
            db,
            order_obj,
            commit=False,
            send_email=False,
        )

        order_obj.product.total_num_sales = order_obj.product.total_num_sales + 1
        order_obj.product.last_sale_price_delta = (
            order_obj.price - order_obj.product.last_sale_price
            if order_obj.product.last_sale_price
            else None
        )
        order_obj.product.last_sale_price = order_obj.price
        db.add(order_obj.product)
        db.flush()

    dispatch_order_confirmation_side_effects(db, order_obj)
    if coupon_obj is not None:
        send_new_coupon_email_for_coupon(coupon_obj)


def get_order_confirmation_side_effects_state(
    order_obj: models.Order,
) -> Dict[str, bool]:
    """Return persisted confirmation side-effect status for an order."""

    props = order_obj.props if isinstance(order_obj.props, dict) else {}
    side_effects_state = props.get(ORDER_CONFIRMATION_SIDE_EFFECTS_KEY)
    if not isinstance(side_effects_state, dict):
        return {}
    return {
        key: bool(value)
        for key, value in side_effects_state.items()
        if isinstance(key, str)
    }


def mark_order_confirmation_side_effect_complete(
    db: Session,
    order_obj: models.Order,
    side_effect_key: str,
) -> None:
    """Persist that a confirmation side effect has completed."""

    side_effects_state = get_order_confirmation_side_effects_state(order_obj)
    if side_effects_state.get(side_effect_key):
        return None

    updated_side_effects_state = dict(side_effects_state)
    updated_side_effects_state[side_effect_key] = True

    props = dict(order_obj.props or {})
    props[ORDER_CONFIRMATION_SIDE_EFFECTS_KEY] = updated_side_effects_state
    order_obj.props = props
    db.add(order_obj)
    db.flush()
    return None


def clear_order_confirmation_side_effect_complete(
    db: Session,
    order_obj: models.Order,
    side_effect_key: str,
) -> None:
    """Clear persisted confirmation side-effect status for an order."""

    side_effects_state = get_order_confirmation_side_effects_state(order_obj)
    if not side_effects_state.get(side_effect_key):
        return None

    updated_side_effects_state = dict(side_effects_state)
    updated_side_effects_state.pop(side_effect_key, None)

    props = dict(order_obj.props or {})
    if updated_side_effects_state:
        props[ORDER_CONFIRMATION_SIDE_EFFECTS_KEY] = updated_side_effects_state
    else:
        props.pop(ORDER_CONFIRMATION_SIDE_EFFECTS_KEY, None)
    order_obj.props = props
    db.add(order_obj)
    db.flush()
    return None


def get_order_confirmation_round_state(db: Session) -> Dict[str, int]:
    """Return current round state without persisting unrelated DB updates."""

    site_globals = (
        db.query(models.Globals.active_round, models.Globals.selling_round)
        .filter(models.Globals.id == 0)
        .one_or_none()
    )
    if site_globals is not None:
        return {
            "active_round": site_globals.active_round,
            "selling_round": site_globals.selling_round,
        }

    active_round = numerai.get_numerai_active_round()
    return {
        "active_round": active_round["number"],
        "selling_round": crud.globals.get_selling_round(active_round),
    }


def dispatch_order_confirmation_side_effects(
    db: Session, order_obj: models.Order
) -> None:
    """Dispatch confirmation follow-up work."""
    side_effects_state = get_order_confirmation_side_effects_state(order_obj)
    round_state = get_order_confirmation_round_state(db)
    active_round = round_state["active_round"]
    selling_round = round_state["selling_round"]
    pending_side_effects: List[Dict[str, Callable[[], None]]] = []
    if (
        selling_round == active_round and order_obj.submit_model_id
        and order_obj.submit_state not in {"queued", "completed"}
        and not side_effects_state.get(ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY)
    ):  # if round open
        print(f"Round {active_round} is open, search for artifact to upload")
        artifacts = crud.artifact.get_multi_by_product_round(
            db,
            product=order_obj.product,
            round_tournament=selling_round,
        )
        if artifacts:
            csv_artifacts = [
                artifact
                for artifact in artifacts
                if artifact.object_name.endswith(".csv")  # type: ignore
            ]
            if csv_artifacts:
                csv_artifact = csv_artifacts[-1]
                bucket = deps.get_gcs_bucket()
                blob = bucket.blob(csv_artifact.object_name)
                if blob.exists():
                    pending_side_effects.append(
                        {
                            "key": ORDER_CONFIRMATION_UPLOAD_ENQUEUED_KEY,
                            "run": lambda csv_artifact=csv_artifact: (
                                print(
                                    f"Uploading csv artifact {csv_artifact.object_name} "
                                    f"for order {order_obj.id}"
                                ),
                                enqueue_upload_numerai_artifact(
                                    order_id=order_obj.id,
                                    object_name=csv_artifact.object_name,
                                    model_id=order_obj.submit_model_id,
                                    numerai_api_key_public_id=order_obj.buyer.numerai_api_key_public_id,
                                    numerai_api_key_secret=order_obj.buyer.numerai_api_key_secret,
                                    tournament=order_obj.product.model.tournament,
                                    version=1,
                                ),
                            ),
                        }
                    )

    # trigger webhook if available
    if not side_effects_state.get(ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY):
        pending_side_effects.append(
            {
                "key": ORDER_CONFIRMATION_WEBHOOK_ENQUEUED_KEY,
                "run": lambda: enqueue_trigger_webhook_for_product(
                    order_obj.product_id, order_obj.id
                ),
            }
        )

    # send order confirmation email
    if not side_effects_state.get(ORDER_CONFIRMATION_EMAILS_SENT_KEY):
        pending_side_effects.append(
            {
                "key": ORDER_CONFIRMATION_EMAILS_SENT_KEY,
                "run": lambda: send_order_confirmation_emails(order_obj),
            }
        )

    for side_effect in pending_side_effects:
        mark_order_confirmation_side_effect_complete(
            db,
            order_obj,
            side_effect["key"],
        )
        side_effects_state[side_effect["key"]] = True

    db.commit()
    db.refresh(order_obj)

    for idx, side_effect in enumerate(pending_side_effects):
        try:
            side_effect["run"]()
        except Exception:
            for failed_side_effect in pending_side_effects[idx:]:
                clear_order_confirmation_side_effect_complete(
                    db,
                    order_obj,
                    failed_side_effect["key"],
                )
            db.commit()
            db.refresh(order_obj)
            raise


def schedule_initial_payment_update(order_obj: models.Order) -> None:
    """Best-effort initial payment enqueue after order creation."""

    if order_obj.currency != "NMR" or settings.ASYNC_OWNER_PAYMENTS != "gcp":
        return None
    try:
        enqueue_update_payment(order_obj.id)
    except Exception:  # pylint: disable=broad-except
        logging.exception(
            "Failed to enqueue initial payment update for order %s", order_obj.id
        )
        try:
            celery_app.send_task(
                "app.worker.update_payment_subtask",
                args=[order_obj.id],
                countdown=settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
            )
        except Exception:  # pylint: disable=broad-except
            logging.exception(
                "Failed to queue legacy payment reconciliation fallback for order %s",
                order_obj.id,
            )
    return None


def update_payment(db: Session, order_id: int) -> None:
    """Update payment for order"""
    order_obj = (
        db.query(models.Order)
        .options(lazyload("*"))
        .filter(models.Order.id == order_id)
        .with_for_update()
        .first()
    )
    if order_obj:
        if order_obj.state == "confirmed":
            on_order_confirmed(db, order_obj, order_obj.transaction_hash)
            return None
        if order_obj.state != "pending":
            return None
        if order_obj.currency == "NMR":
            # handle 100% discount
            if order_obj.price == 0:
                on_order_confirmed(db, order_obj, transaction=None)

            matched_transaction = match_transaction_for_order(db, order_obj)
            # handle manual confirmation
            if matched_transaction is None and order_obj.transaction_hash is not None:
                matched_transaction = order_obj.transaction_hash

            # trigger confirmation events
            if matched_transaction is not None:
                on_order_confirmed(db, order_obj, matched_transaction)

            # expiration
            if (
                order_obj.state != "confirmed"
                and datetime.now() - order_obj.date_order
                > timedelta(minutes=settings.PENDING_ORDER_EXPIRE_MINUTES)
            ):
                print(f"Order {order_id} expired")
                order_obj.state = "expired"
                db.commit()
                db.refresh(order_obj)

                send_order_expired_emails(order_obj)
        else:
            order_obj.state = "invalid_currency"
            db.commit()
            db.refresh(order_obj)


def send_order_confirmation_emails(order_obj: models.Order) -> None:
    """Send order confirmation emails"""
    if settings.EMAILS_ENABLED:
        product = order_obj.product
        # Send seller email
        if product.owner.email:
            send_new_confirmed_sale_email(
                email_to=product.owner.email,
                username=product.owner.username,
                round_order=order_obj.round_order,
                date_order=order_obj.date_order,
                product=product.sku,
                buyer=order_obj.buyer.username,
                transaction_hash=order_obj.transaction_hash,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
                use_encryption=(order_obj.buyer_public_key is not None),  # type: ignore
            )

        # Send buyer email
        if order_obj.buyer.email:
            send_order_confirmed_email(
                email_to=order_obj.buyer.email,
                username=order_obj.buyer.username,
                round_order=order_obj.round_order,
                date_order=order_obj.date_order,
                product=product.sku,
                from_address=order_obj.from_address,  # type: ignore
                to_address=order_obj.to_address,  # type: ignore
                transaction_hash=order_obj.transaction_hash,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
            )


def send_order_expired_emails(order_obj: models.Order) -> None:
    """Send order expired emails"""
    if settings.EMAILS_ENABLED:
        # Send buyer email
        product = order_obj.product
        if order_obj.buyer.email:
            send_order_expired_email(
                email_to=order_obj.buyer.email,
                username=order_obj.buyer.username,
                round_order=order_obj.round_order,
                date_order=order_obj.date_order,
                product=product.sku,
                from_address=order_obj.from_address,  # type: ignore
                to_address=order_obj.to_address,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
            )


def send_order_canceled_emails(order_obj: models.Order) -> None:
    """Send order canceled emails"""
    if settings.EMAILS_ENABLED:
        # Send buyer email
        product = order_obj.product
        if order_obj.buyer.email:
            send_order_canceled_email(
                email_to=order_obj.buyer.email,
                username=order_obj.buyer.username,
                round_order=order_obj.round_order,
                date_order=order_obj.date_order,
                product=product.sku,
                from_address=order_obj.from_address,  # type: ignore
                to_address=order_obj.to_address,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
            )


def send_failed_autosubmit_emails(order_obj: models.Order, artifact_name: str) -> None:
    """Send failed auto-submit emails"""
    if settings.EMAILS_ENABLED:
        product = order_obj.product
        # Send seller auto-submit failure email
        if product.owner.email:
            send_failed_autosubmit_seller_email(
                email_to=product.owner.email,
                username=product.owner.username,
                buyer=order_obj.buyer.username,
                model=order_obj.submit_model_name,  # type: ignore
                artifact=artifact_name,
                order_id=order_obj.id,
                round_tournament=order_obj.round_order,
                product=product.sku,
            )

        # Send buyer auto-submit failure email
        if order_obj.buyer.email:
            send_failed_autosubmit_buyer_email(
                email_to=order_obj.buyer.email,
                username=order_obj.buyer.username,
                model=order_obj.submit_model_name,  # type: ignore
                artifact=artifact_name,
                order_id=order_obj.id,
                round_tournament=order_obj.round_order,
                product=product.sku,
            )


def send_order_upload_reminder_emails(order_obj: models.Order) -> None:
    """Send order upload reminder emails"""
    if settings.EMAILS_ENABLED:
        # Send upload email reminder to seller
        if order_obj.product.owner.email:
            send_order_artifact_upload_reminder_email(
                email_to=order_obj.product.owner.email,
                username=order_obj.product.owner.username,
                order_id=order_obj.id,  # type: ignore
                round_order=order_obj.round_order,  # type: ignore
                product=order_obj.product.sku,
                buyer=order_obj.buyer.username,  # type: ignore
            )


def send_order_refund_request_emails(
    order_obj: models.Order,
    wallet: str,
    contact: Optional[str] = None,
    message: Optional[str] = None,
) -> None:
    """Send order refund request emails"""
    if settings.EMAILS_ENABLED:
        # Send refund request to seller
        if order_obj.product.owner.email:
            send_order_refund_request_email(
                email_to=order_obj.product.owner.email,
                username=order_obj.product.owner.username,
                order_id=order_obj.id,  # type: ignore
                round_order=order_obj.round_order,  # type: ignore
                product=order_obj.product.sku,
                buyer=order_obj.buyer.username,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
                wallet=wallet,
                contact=contact or "-",
                message=message or "-",
            )
