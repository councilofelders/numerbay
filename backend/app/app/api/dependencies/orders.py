""" Dependencies for orders endpoints """

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.coupons import create_coupon_for_order
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


def validate_existing_order(db: Session, order_id: int) -> models.Order:
    """Validate existing order"""
    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def get_order_weekend_round_numbers(round_order: int, quantity: int) -> List[int]:
    original_end_round = round_order + quantity - 1
    if original_end_round <= 339:
        return list(range(round_order, round_order + quantity))
    else:
        daily_base_round = max(339, round_order)
        daily_quantity = original_end_round - daily_base_round
        return list(range(round_order, 339)) + list(
            range(daily_base_round, daily_base_round + daily_quantity * 5 + 1, 5)
        )


def any_weekday_round(rounds_numbers: List[int]) -> bool:
    for round_number in rounds_numbers:
        if round_number <= 339:
            continue
        if ((round_number - 339) % 5) != 0:
            return True
    return False


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
            if transaction["to"] == order_obj.to_address:
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
    # update order
    # order_obj.transaction_hash = transaction
    # order_obj.state = "confirmed"
    # db.commit()
    # db.refresh(order_obj)
    crud.order.update(
        db,
        db_obj=order_obj,
        obj_in={"transaction_hash": transaction, "state": "confirmed"},
    )

    # Generate coupon if applicable
    create_coupon_for_order(db, order_obj)

    # Update product sales stats
    crud.product.update(
        db,
        db_obj=order_obj.product,
        obj_in={
            "total_num_sales": order_obj.product.total_num_sales + 1,
            "last_sale_price_delta": order_obj.price - order_obj.product.last_sale_price
            if order_obj.product.last_sale_price
            else None,
            "last_sale_price": order_obj.price,
        },
    )

    # Upload csv artifact for order if round open
    site_globals = crud.globals.update_singleton(db)
    selling_round = site_globals.selling_round  # type: ignore
    if (
        selling_round == site_globals.active_round and order_obj.submit_model_id
    ):  # if round open
        print(
            f"Round {site_globals.active_round} is open, search for artifact to upload"
        )
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
                    print(
                        f"Uploading csv artifact {csv_artifact.object_name} "
                        f"for order {order_obj.id}"
                    )
                    celery_app.send_task(
                        "app.worker.upload_numerai_artifact_task",
                        kwargs=dict(
                            order_id=order_obj.id,
                            object_name=csv_artifact.object_name,
                            model_id=order_obj.submit_model_id,
                            numerai_api_key_public_id=order_obj.buyer.numerai_api_key_public_id,
                            numerai_api_key_secret=order_obj.buyer.numerai_api_key_secret,
                            tournament=order_obj.product.model.tournament,
                            version=1,
                        ),
                    )

    # trigger webhook if available
    celery_app.send_task(
        "app.worker.trigger_webhook_for_product_task",
        args=[order_obj.product_id, order_obj.id],
    )

    # send order confirmation email
    send_order_confirmation_emails(order_obj)


def update_payment(db: Session, order_id: int) -> None:
    """Update payment for order"""
    order_obj = crud.order.get(db, id=order_id)
    if order_obj:
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
