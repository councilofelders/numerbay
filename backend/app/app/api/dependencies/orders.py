from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

import pandas as pd
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.coupons import create_coupon_for_order
from app.core.celery_app import celery_app
from app.core.config import settings
from app.utils import (
    send_new_confirmed_sale_email,
    send_order_confirmed_email,
    send_order_expired_email,
)


def match_transaction_for_order(db: Session, order_obj: models.Order) -> Optional[str]:
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
    except Exception:
        pass
    return matched_transaction


def on_order_confirmed(db: Session, order_obj: models.Order, transaction: str) -> None:
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
    globals = crud.globals.update_singleton(db)
    selling_round = globals.selling_round  # type: ignore
    if (
        selling_round == globals.active_round and order_obj.submit_model_id
    ):  # if round open
        print(f"Round {globals.active_round} is open, search for artifact to upload")
        artifacts = crud.artifact.get_multi_by_product_round(
            db, product=order_obj.product, round_tournament=selling_round,
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

    send_order_confirmation_emails(order_obj)


def update_payment(db: Session, order_id: int) -> None:
    order_obj = crud.order.get(db, id=order_id)
    if order_obj:
        if order_obj.currency == "NMR":
            matched_transaction = match_transaction_for_order(db, order_obj)
            # handle manual confirmation
            if matched_transaction is None and order_obj.transaction_hash is not None:
                matched_transaction = order_obj.transaction_hash

            # trigger confirmation events
            if matched_transaction is not None:
                on_order_confirmed(db, order_obj, matched_transaction)

            # expiration
            if order_obj.state != "confirmed" and datetime.now() - order_obj.date_order > timedelta(
                minutes=settings.PENDING_ORDER_EXPIRE_MINUTES
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
    return


def send_order_confirmation_emails(order_obj: models.Order) -> None:
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
                from_address=order_obj.from_address,  # type: ignore
                to_address=order_obj.to_address,  # type: ignore
                transaction_hash=order_obj.transaction_hash,  # type: ignore
                amount=order_obj.price,
                currency=order_obj.currency,  # type: ignore
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
