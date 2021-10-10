import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from app.core.celery_app import celery_app
from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
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
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
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


def send_new_order_email(
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
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New order for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_order.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/order-history"
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


def send_new_confirmed_sale_email(
    email_to: str,
    username: str,
    round_order: int,
    date_order: datetime,
    product: str,
    buyer: str,
    from_address: str,
    to_address: str,
    transaction_hash: str,
    amount: float,
    currency: str,
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New confirmed sale for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_confirmed_sale.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/sales-history"
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
                "from_address": from_address,
                "to_address": to_address,
                "transaction_hash": transaction_hash,
                "amount": amount,
                "currency": currency,
                "link": link,
            },
        ),
    )


def send_order_confirmed_email(
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
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Order confirmed for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "order_confirmed.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/order-history"
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


def send_order_expired_email(
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
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Order expired for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "order_expired.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/order-history"
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
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New artifact for order for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_artifact.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/order-history"
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
    email_to: str, username: str, round_tournament: int, product: str, artifact: str,
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New artifact added for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_artifact_seller.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/my-listings"
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


def send_failed_artifact_seller_email(
    email_to: str, username: str, round_tournament: int, product: str, artifact: str,
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Failed artifact upload for {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "failed_artifact_seller.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST + "/my-account/my-listings"
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


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
