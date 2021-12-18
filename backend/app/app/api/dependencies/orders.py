from app import models
from app.core.config import settings
from app.utils import (
    send_new_confirmed_sale_email,
    send_order_confirmed_email,
    send_order_expired_email,
)


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
