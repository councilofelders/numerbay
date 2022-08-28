""" App util functions """

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from app.core.celery_app import celery_app
from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict = None,
) -> None:
    """
    Generic function for sending emails

    Args:
        email_to (str): recipient email
        subject_template (str): email subject
        html_template (str): email template
        environment (dict): env variables for email template
    """
    if environment is None:
        environment = {}
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    """
    Send test email

    Args:
        email_to (str): recipient email
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    """
    Send reset password email (placeholder, not used)

    Args:
        email_to (str): recipient email
        email (str): account email
        token (str): password reset token
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for {email}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


# def send_new_account_email(email_to: str, username: str, password: str) -> None:
#     project_name = settings.PROJECT_NAME
#     subject = f"{project_name} - New account for {username}"
#     with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
#         template_str = f.read()
#     link = settings.SERVER_HOST
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": settings.PROJECT_NAME,
#             "username": username,
#             "password": password,
#             "email": email_to,
#             "link": link,
#         },
#     )


def send_new_order_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    timeout: int,
    round_order: int,
    date_order: datetime,
    product: str,
    from_address: str,
    to_address: str,
    amount: float,
    currency: str,
) -> None:
    """
    Send new order email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        timeout (int): timeout for sending email
        round_order (int): tournament round for order
        date_order (datetime): datetime for order
        product (str): product full name
        from_address (str): buyer wallet address
        to_address (str): seller wallet address
        amount (float): order price amount
        currency (str): order currency
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New order for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "new_order.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "timeout": timeout,
                "round_order": round_order,
                "date_order": date_order,
                "product": product,
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "currency": currency,
                "link": link,
            },
        ),
    )
    # send_email(
    #     email_to=email_to,
    #     subject_template=subject,
    #     html_template=template_str,
    #     environment={
    #         "project_name": "NumerBay",
    #         "username": username,
    #         "date_order": date_order,
    #         "product": product,
    #         "from_address": from_address,
    #         "to_address": to_address,
    #         "amount": amount,
    #         "currency": currency,
    #         "link": link,
    #     },
    # )


def send_new_confirmed_sale_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    round_order: int,
    date_order: datetime,
    product: str,
    buyer: str,
    transaction_hash: str,
    amount: float,
    currency: str,
    use_encryption: bool,
) -> None:
    """
    Send new confirmed sale email

    Args:
        email_to (str): recipient email
        username (str): seller username
        round_order (int): tournament round for order
        date_order (datetime): datetime for order
        product (str): product full name
        buyer (str): buyer username
        transaction_hash (str): transaction hash
        amount (float): order price amount
        currency (str): order currency
        use_encryption (bool): whether the order uses client-side encryption
    """
    subject = f"{settings.PROJECT_NAME} - New confirmed sale for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "new_confirmed_sale.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/sales"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_order": round_order,
                "date_order": date_order,
                "product": product,
                "buyer": buyer,
                "transaction_hash": transaction_hash,
                "amount": amount,
                "currency": currency,
                "link": link,
                "use_encryption": use_encryption,
            },
        ),
    )


def send_order_confirmed_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    round_order: int,
    date_order: datetime,
    product: str,
    from_address: str,
    to_address: str,
    transaction_hash: str,
    amount: float,
    currency: str,
) -> None:
    """
    Send order confirmed email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        round_order (int): tournament round for order
        date_order (datetime): datetime for order
        product (str): product full name
        from_address (str): buyer wallet address
        to_address (str): seller wallet address
        transaction_hash (str): transaction hash
        amount (float): order price amount
        currency (str): order currency
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Order confirmed for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "order_confirmed.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_order": round_order,
                "date_order": date_order,
                "product": product,
                "from_address": from_address,
                "to_address": to_address,
                "transaction_hash": transaction_hash,
                "amount": amount,
                "currency": currency,
                "link": link,
            },
        ),
    )


def send_order_expired_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    round_order: int,
    date_order: datetime,
    product: str,
    from_address: str,
    to_address: str,
    amount: float,
    currency: str,
) -> None:
    """
    Send order expired email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        round_order (int): tournament round for order
        date_order (datetime): datetime for order
        product (str): product full name
        from_address (str): buyer wallet address
        to_address (str): seller wallet address
        amount (float): order price amount
        currency (str): order currency
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Order expired for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "order_expired.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_order": round_order,
                "date_order": date_order,
                "product": product,
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "currency": currency,
                "link": link,
            },
        ),
    )


def send_order_canceled_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    round_order: int,
    date_order: datetime,
    product: str,
    from_address: str,
    to_address: str,
    amount: float,
    currency: str,
) -> None:
    """
    Send order canceled email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        round_order (int): tournament round for order
        date_order (datetime): datetime for order
        product (str): product full name
        from_address (str): buyer wallet address
        to_address (str): seller wallet address
        amount (float): order price amount
        currency (str): order currency
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Order canceled for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "order_canceled.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_order": round_order,
                "date_order": date_order,
                "product": product,
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "currency": currency,
                "link": link,
            },
        ),
    )


def send_new_artifact_email(
    email_to: str,
    username: str,
    round_order: int,
    product: str,
    order_id: int,
    artifact: str,
) -> None:
    """
    Send new artifact email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        round_order (int): tournament round for order
        product (str): product full name
        order_id (int): order id
        artifact (str): artifact name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New artifact for order for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "new_artifact.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_order": round_order,
                "product": product,
                "order_id": order_id,
                "artifact": artifact,
                "link": link,
            },
        ),
    )


def send_new_artifact_seller_email(
    email_to: str,
    username: str,
    round_tournament: int,
    product: str,
    artifact: str,
) -> None:
    """
    Send new artifact seller email

    Args:
        email_to (str): recipient email
        username (str): seller username
        round_tournament (int): tournament round
        product (str): product full name
        artifact (str): artifact name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New artifact added for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "new_artifact_seller.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/listings"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_tournament": round_tournament,
                "product": product,
                "artifact": artifact,
                "link": link,
            },
        ),
    )


def send_new_coupon_email(  # pylint: disable=too-many-arguments
    email_to: str,
    username: str,
    code: str,
    date_expiration: datetime,
    applicable_product_ids: Optional[List[int]],
    min_spend: Optional[float],
    max_discount: Optional[float],
    discount_percent: int,
    quantity_total: int,
    message: Optional[str] = None,
) -> None:
    """
    Send new coupon email

    Args:
        email_to (str): recipient email
        username (str): coupon owner username
        code (str): coupon code
        date_expiration (datetime): coupon expiration date
        applicable_product_ids (list): list of applicable product ids for coupon
        min_spend (float, optional): minimum spend for coupon
        max_discount (float, optional): maximum discount amount for coupon
        discount_percent (int): discount percentage (0-100) for coupon
        quantity_total (int): coupon total quantity
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New coupon available for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "new_coupon.html", encoding="utf8"
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/coupons"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "code": code,
                "date_expiration": date_expiration,
                "applicable_product_ids": applicable_product_ids,
                "min_spend": min_spend,
                "max_discount": max_discount,
                "discount_percent": discount_percent,
                "quantity_total": quantity_total,
                "message": message,
                "link": link,
            },
        ),
    )


def send_failed_artifact_seller_email(
    email_to: str,
    username: str,
    round_tournament: int,
    product: str,
    artifact: str,
) -> None:
    """
    Send failed artifact seller email

    Args:
        email_to (str): recipient email
        username (str): seller username
        round_tournament (int): tournament round
        product (str): product full name
        artifact (str): artifact name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Failed artifact upload for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "failed_artifact_seller.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/listings"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "round_tournament": round_tournament,
                "product": product,
                "artifact": artifact,
                "link": link,
            },
        ),
    )


def send_order_artifact_upload_reminder_email(
    email_to: str,
    username: str,
    order_id: int,
    round_order: int,
    product: str,
    buyer: str,
) -> None:
    """
    Send order artifact upload reminder email

    Args:
        email_to (str): recipient email
        username (str): seller username
        order_id (int): order id
        round_order (int): tournament round for order
        product (str): product full name
        buyer (str): buyer username
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Reminder to upload for {buyer}'s order"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "order_artifact_upload_reminder.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/listings"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "order_id": order_id,
                "round_order": round_order,
                "product": product,
                "buyer": buyer,
                "link": link,
            },
        ),
    )


def send_order_refund_request_email(
    email_to: str,
    username: str,
    order_id: int,
    round_order: int,
    product: str,
    buyer: str,
    amount: float,
    currency: str,
    wallet: str,
    contact: str,
    message: str,
) -> None:
    """
    Send order refund request email

    Args:
        email_to (str): recipient email
        username (str): seller username
        order_id (int): order id
        round_order (int): tournament round for order
        product (str): product full name
        buyer (str): buyer username
        amount (float): order price amount
        currency (str): order currency
        wallet (str): buyer wallet to refund to
        contact (str): buyer contact
        message (str): short message from buyer
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Refund request for {buyer}'s order"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "order_refund_request.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/sales"
    print(
        dict(
            email_to=email_to,
            subject_template=subject,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "order_id": order_id,
                "round_order": round_order,
                "product": product,
                "buyer": buyer,
                "amount": amount,
                "currency": currency,
                "wallet": wallet,
                "contact": contact,
                "message": message,
                "link": link,
            },
        )
    )
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "order_id": order_id,
                "round_order": round_order,
                "product": product,
                "buyer": buyer,
                "amount": amount,
                "currency": currency,
                "wallet": wallet,
                "contact": contact,
                "message": message,
                "link": link,
            },
        ),
    )


def send_succeeded_webhook_email(
    email_to: str,
    username: str,
    date: str,
    product: str,
) -> None:
    """
    Send succeeded webhook email

    Args:
        email_to (str): recipient email
        username (str): seller username
        date (str): iso date string
        product (str): product full name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Webhook trigger success for {product}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "webhook_success.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/sales"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "date": date,
                "product": product,
                "link": link,
            },
        ),
    )


def send_failed_webhook_email(
    email_to: str,
    username: str,
    date: str,
    product: str,
) -> None:
    """
    Send failed webhook email

    Args:
        email_to (str): recipient email
        username (str): seller username
        date (str): iso date string
        product (str): product full name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Failed webhook trigger for {product}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "webhook_failed.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/sales"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "date": date,
                "product": product,
                "link": link,
            },
        ),
    )


def send_failed_autosubmit_seller_email(
    email_to: str,
    username: str,
    buyer: str,
    model: str,
    artifact: str,
    order_id: int,
    round_tournament: int,
    product: str,
) -> None:
    """
    Send failed auto-submit seller email

    Args:
        email_to (str): recipient email
        username (str): seller username
        buyer (str): buyer username
        model (str): model username
        order_id (int): order ID
        round_tournament (int): tournament round
        product (str): product full name
        artifact (str): artifact name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Failed auto-submission for buyer {buyer}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "failed_autosubmit_seller.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/sales"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "buyer": buyer,
                "model": model,
                "artifact": artifact,
                "order_id": order_id,
                "round_tournament": round_tournament,
                "product": product,
                "link": link,
            },
        ),
    )


def send_failed_autosubmit_buyer_email(
    email_to: str,
    username: str,
    model: str,
    artifact: str,
    order_id: int,
    round_tournament: int,
    product: str,
) -> None:
    """
    Send failed auto-submit buyer email

    Args:
        email_to (str): recipient email
        username (str): buyer username
        model (str): model name
        order_id (int): order ID
        round_tournament (int): tournament round
        product (str): product full name
        artifact (str): artifact name
    """
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Failed auto-submission for {username}"
    with open(
        Path(settings.EMAIL_TEMPLATES_DIR) / "failed_autosubmit_buyer.html",
        encoding="utf8",
    ) as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/purchases"
    celery_app.send_task(
        "app.worker.send_email_task",
        kwargs=dict(
            email_to=email_to,
            subject_template=subject,
            html_template=template_str,
            environment={
                "project_name": "NumerBay",
                "username": username,
                "model": model,
                "artifact": artifact,
                "order_id": order_id,
                "round_tournament": round_tournament,
                "product": product,
                "link": link,
            },
        ),
    )


def generate_password_reset_token(email: str) -> str:
    """
    Generate password reset token (placeholder, not used)

    Args:
        email (str): account email

    Returns:
        str: password reset token
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify password reset token (placeholder, not used)

    Args:
        token (str): password reset token

    Returns:
        str: decoded token
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
