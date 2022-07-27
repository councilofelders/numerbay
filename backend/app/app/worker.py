""" Celery worker tasks """

import functools
import io
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

import pandas as pd
import requests
from celery import group
from celery.schedules import crontab
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import NotFound
from raven import Client
from sqlalchemy import and_, func, select

from app import crud
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.artifacts import send_artifact_emails_for_active_orders
from app.api.dependencies.order_artifacts import generate_gcs_signed_url
from app.api.dependencies.orders import send_failed_autosubmit_emails, update_payment
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import (
    Artifact,
    Category,
    Model,
    Order,
    OrderArtifact,
    Poll,
    Product,
    StakeSnapshot,
)
from app.utils import (
    send_email,
    send_failed_artifact_seller_email,
    send_failed_webhook_email,
    send_new_artifact_email,
    send_new_artifact_seller_email,
    send_order_artifact_upload_reminder_email,
    send_succeeded_webhook_email,
)

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    """
    Test celery task

    Args:
        word (str): message to send
    """

    return f"test task return {word}"


@celery_app.task
def tick(msg: str) -> str:
    """
    Simple tick task

    Args:
        msg (str): message to send
    """

    print(f"Tick! The time is: {datetime.now()}, arg: {msg}")
    sys.stdout.flush()

    time.sleep(2)
    return msg


@celery_app.task  # (acks_late=True)
def send_email_task(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict = None,
) -> None:
    """
    Generic task for sending emails

    Args:
        email_to (str): recipient email
        subject_template (str): email subject
        html_template (str): email template
        environment (dict): env variables for email template
    """

    if environment is None:
        environment = {}
    send_email(
        email_to=email_to,
        subject_template=subject_template,
        html_template=html_template,
        environment=environment,
    )


@celery_app.task  # (acks_late=True)
def send_new_artifact_emails_task(artifact_id: int) -> None:
    """
    Send new artifact email task

    Args:
        artifact_id (int): artifact id
    """
    if settings.EMAILS_ENABLED:
        db = SessionLocal()
        try:
            artifact = crud.artifact.get(db, id=artifact_id)

            if not artifact:
                return None

            send_artifact_emails_for_active_orders(db, artifact)
        finally:
            db.close()
    return None


@celery_app.task  # (acks_late=True)
def send_new_order_artifact_emails_task(artifact_id: str) -> None:
    """
    Send new order artifact email task

    Args:
        artifact_id (str): order artifact id
    """
    if settings.EMAILS_ENABLED:
        db = SessionLocal()
        try:
            artifact = crud.order_artifact.get(db, id=artifact_id)

            if not artifact:
                return None

            order = artifact.order

            # Send new artifact email notifications to buyers
            if order.buyer.email:
                send_new_artifact_email(
                    email_to=order.buyer.email,
                    username=order.buyer.username,
                    round_order=order.round_order,
                    product=order.product.sku,
                    order_id=order.id,
                    artifact=artifact.object_name,  # type: ignore
                )

            # Send new artifact email notification to seller
            if order.product.owner.email:
                send_new_artifact_seller_email(
                    email_to=order.product.owner.email,
                    username=order.product.owner.username,
                    round_tournament=artifact.round_tournament,  # type: ignore
                    product=order.product.sku,
                    artifact=artifact.object_name,  # type: ignore
                )
        finally:
            db.close()
    return None


@celery_app.task  # (acks_late=True)
def send_order_artifact_upload_reminder_emails_task() -> None:
    """Send order artifact upload reminder emails task"""
    if not settings.EMAILS_ENABLED:
        return None
    db = SessionLocal()
    try:
        selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

        orders = crud.order.get_active_orders(db, round_order=selling_round)
        orders_to_remind = []
        for order in orders:
            if order.buyer_public_key is None:  # skip for non per-order artifacts
                continue
            requires_numerai_submission = order.submit_model_id is not None
            requires_file = order.mode == "file"
            has_numerai_submission = False
            has_file = False
            # if not isinstance(order.artifacts, list):
            #     continue
            for artifact in order.artifacts:  # type: ignore
                if artifact.state == "active":
                    if artifact.is_numerai_direct:
                        has_numerai_submission = True
                    else:
                        has_file = True

            if (requires_numerai_submission and not has_numerai_submission) or (
                requires_file and not has_file
            ):
                orders_to_remind.append(order)

        for order in orders_to_remind:
            # Send new artifact email notification to seller
            if order.product.owner.email:
                send_order_artifact_upload_reminder_email(
                    email_to=order.product.owner.email,
                    username=order.product.owner.username,
                    order_id=order.round_order,  # type: ignore
                    round_order=order.round_order,  # type: ignore
                    product=order.product.sku,
                    buyer=order.buyer.username,  # type: ignore
                )
    finally:
        db.close()
    return None


@celery_app.task  # (acks_late=True)
def update_model_subtask(user_json: Dict, retries: int = 0) -> Optional[Any]:
    """
    Update individual user's Numerai models subtask

    Args:
        user_json (dict): dict of user information
        retries (int): number of retries
    """
    db = SessionLocal()

    try:
        # Update user info
        user_has_valid_numerai_api = crud.user.update_numerai_api(db, user_json)

        # Update user models
        updated_username = None
        if user_has_valid_numerai_api:
            updated_username = crud.model.update_model(db, user_json)

        # Handled users that failed authenticated updates
        if updated_username is None:
            print(f"Trying to update user {user_json['username']} without auth")
            crud.model.update_model_unauthenticated(db, user_json)
    except Exception as e:  # pylint: disable=broad-except
        print(
            f"Error updating model scores for user {user_json['username']}: "
            f"[{e}], {retries} retries remaining"
        )
        if retries > 0:
            print(
                f"Retrying updating model scores for user {user_json['username']} "
                f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS} seconds"
            )
            celery_app.send_task(
                "app.worker.update_model_subtask",
                countdown=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
                kwargs=dict(user_json=user_json, retries=retries - 1),
            )
    finally:
        db.close()
    return None


@celery_app.task  # (acks_late=True)
def batch_update_models_task() -> None:
    """Batch upload Numerai models task"""
    db = SessionLocal()
    try:
        users = crud.user.search(
            # type: ignore
            db,
            filters={"numerai_api_key_public_id": ["any"]},
            limit=None,
        )["data"]
        print(f"total: {len(users)}")
        # result = chord([fetch_model_subtask.s(jsonable_encoder(user), 0) for user in users],
        # commit_models_subtask.s(0)).delay()
        group(
            [
                update_model_subtask.s(jsonable_encoder(user), retries=10).set(
                    countdown=i // 5
                )
                for i, user in enumerate(users)
            ]
        ).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_model_scores_task(retries: int = 0) -> None:
    """
    Batch update Numerai models scores task

    Args:
        retries (int): number of tries
    """
    try:
        pipeline_status = numerai.get_numerai_pipeline_status(tournament=8)
        if pipeline_status["isScoringDay"]:
            if pipeline_status.get("resolvedAt", None):
                print("Numerai pipeline completed, update model scores...")
                db = SessionLocal()
                try:
                    users = crud.user.search(
                        # type: ignore
                        db,
                        filters={"numerai_api_key_public_id": ["any"]},
                        limit=None,
                    )["data"]
                    print(f"total: {len(users)}")
                    # result = chord([fetch_model_subtask
                    # .s(jsonable_encoder(user), 0) for user in users],
                    # commit_models_subtask.s(0)).delay()
                    group(
                        [
                            update_model_subtask.s(
                                jsonable_encoder(user), retries=10
                            ).set(countdown=60 + i // 5)
                            for i, user in enumerate(users)
                        ]
                    ).apply_async()
                finally:
                    db.close()
            else:
                print(
                    f"Numerai pipeline not ready, checking again "
                    f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS}s"
                )
                celery_app.send_task(
                    "app.worker.batch_update_model_scores_task",
                    countdown=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
                    kwargs=dict(retries=retries),
                )
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error starting model scores update [{e}], {retries} retries remaining")
        if retries > 0:
            print(
                f"Retrying starting model scores update "
                f"in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS} seconds"
            )
            celery_app.send_task(
                "app.worker.batch_update_model_scores_task",
                countdown=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
                kwargs=dict(retries=retries - 1),
            )


@celery_app.task  # (acks_late=True)
def update_globals_stats_task() -> None:
    """Update global stats task"""
    db = SessionLocal()
    try:
        crud.globals.update_stats(db)
        crud.stats.update_stats(db)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def update_active_round() -> None:
    """Update active round task"""
    db = SessionLocal()
    try:
        active_round = numerai.get_numerai_active_round()
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()

        active_round_number = active_round["number"]
        print(
            f"UTC time: {utc_time}, round open: {open_time}, "
            f"round close: {close_staking_time}, round: {active_round_number}"
        )

        if open_time <= utc_time <= close_staking_time:  # new round opened and active
            print(f"Round {active_round_number} opened")
            # update active round
            crud.globals.update(
                db,
                db_obj=crud.globals.get_singleton(db),  # type: ignore
                obj_in={"active_round": active_round_number},
            )
            # trigger Numerai submissions
            celery_app.send_task("app.worker.batch_submit_numerai_models_task")
        else:
            # New round not yet opened, try again soon
            celery_app.send_task(
                "app.worker.update_active_round",
                countdown=settings.ROUND_ROLLOVER_POLL_FREQUENCY_SECONDS,
            )
    finally:
        print(
            f"Current global state: {jsonable_encoder(crud.globals.get_singleton(db))}"
        )
        db.close()


@celery_app.task  # (acks_late=True)
def update_round_rollover() -> None:
    """Update round rollover task"""
    db = SessionLocal()
    try:
        site_globals = crud.globals.get_singleton(db)

        active_round = numerai.get_numerai_active_round()
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()
        # next_round_open_time = pd.to_datetime(active_round["closeTime"]).to_pydatetime()

        active_round_number = active_round["number"]
        print(
            f"UTC time: {utc_time}, round open: {open_time}, "
            f"round close: {close_staking_time}, round: {active_round_number}"
        )

        if open_time <= utc_time <= close_staking_time:  # new round opened and active
            print("Activities freezed due to round rollover")
            # freeze activities
            crud.globals.update(
                db,
                db_obj=site_globals,  # type: ignore
                obj_in={"is_doing_round_rollover": True},
            )

            # check order stake
            celery_app.send_task(
                "app.worker.batch_validate_numerai_models_stake_task",
            )

            # check again soon
            celery_app.send_task(
                "app.worker.update_round_rollover",
                countdown=settings.ROUND_ROLLOVER_POLL_FREQUENCY_SECONDS,
            )
        else:  # current round closed for staking, start selling next round, unfreeze activities
            if (
                site_globals.active_round == active_round_number  # type: ignore
                and site_globals.selling_round == active_round_number + 1  # type: ignore
                # type: ignore
            ):  # active round already up-to-date
                print("Round already up-to-date, no action")
            else:
                print("Unfreeze activities, rollover completed")
                selling_rouind = active_round_number + 1
                crud.globals.update(
                    db,
                    db_obj=site_globals,  # type: ignore
                    obj_in={
                        "active_round": active_round_number,
                        "selling_round": selling_rouind,
                        "is_doing_round_rollover": False,
                    },
                )  # update round number and unfreeze
                # expire old products
                crud.product.bulk_expire(
                    db, current_round=site_globals.selling_round  # type: ignore
                )

                # mark order artifacts for pruning
                crud.order_artifact.bulk_mark_for_pruning(
                    db, current_round=site_globals.selling_round  # type: ignore
                )

                # unmark product readiness
                crud.product.bulk_unmark_is_ready(db)
    finally:
        print(
            f"Current global state: {jsonable_encoder(crud.globals.get_singleton(db))}"
        )
        db.close()


@celery_app.task  # (acks_late=True)
def update_payment_subtask(order_id: int) -> None:
    """
    Update payment subtask

    Args:
        order_id (int): order id
    """
    db = SessionLocal()
    try:
        # Update order payment
        update_payment(db, order_id)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_payments_task() -> None:
    """Batch update payments task"""
    db = SessionLocal()
    try:
        orders = crud.order.get_multi_by_state(db, state="pending")
        print(f"total pending orders: {len(orders)}")
        group([update_payment_subtask.s(order.id) for order in orders]).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def upload_numerai_artifact_task(  # pylint: disable=too-many-arguments
    order_id: int,
    object_name: str,
    model_id: str,
    numerai_api_key_public_id: str,
    numerai_api_key_secret: str,
    tournament: int = 8,
    version: int = 1,  # pylint: disable=unused-argument
) -> Optional[Any]:
    """
    Upload Numerai artifact task

    Args:
        order_id (int): order id
        object_name (str): object name
        model_id (str): Numerai model id
        numerai_api_key_public_id (str): Numerai API key public ID
        numerai_api_key_secret (str): Numerai API key secret
        tournament (int): Tournament ID
        version (int): Data version (placeholder, not used)
    """
    db = SessionLocal()
    try:
        order = crud.order.get(db=db, id=order_id)
        if not order:
            print(f"Order {order_id} not found, skipped")
            return None
        # Disable queue check to always redo submission
        # if order.submit_state == "queued":  # already queued for submission
        #     print(f"Order {order.id} already queued for submission, skipped")
        #     return None
        crud.order.update(db, db_obj=order, obj_in={"submit_state": "queued"})
    finally:
        db.close()

    # Has csv artifact and uploaded
    url = generate_gcs_signed_url(
        bucket=deps.get_gcs_bucket(),
        object_name=object_name,
        action="GET",
        expiration_minutes=settings.ARTIFACT_DOWNLOAD_URL_EXPIRE_MINUTES,
        is_upload=False,
    )

    # Upload URL
    submission_auth = numerai.generate_numerai_submission_url(
        object_name=object_name,
        model_id=model_id,
        tournament=tournament,
        numerai_api_key_public_id=numerai_api_key_public_id,
        numerai_api_key_secret=numerai_api_key_secret,
    )

    # Bridge Upload file
    file_stream = requests.get(url, stream=True)
    requests.put(
        submission_auth["url"], data=io.BytesIO(file_stream.content), stream=True
    )

    # Validate Upload
    submission_id = numerai.validate_numerai_submission(
        object_name=submission_auth["filename"],
        model_id=model_id,
        tournament=tournament,
        numerai_api_key_public_id=numerai_api_key_public_id,
        numerai_api_key_secret=numerai_api_key_secret,
    )

    if submission_id:
        # submision successful, mark order submit_state to completed
        db = SessionLocal()
        try:
            order = crud.order.get(db, id=order_id)
            crud.order.update(
                db,
                db_obj=order,  # type: ignore
                obj_in={
                    "submit_state": "completed",
                    "last_submit_round": crud.globals.get_singleton(  # type: ignore
                        db=db
                    ).selling_round,
                },
            )
        finally:
            db.close()
    else:
        # mark failed submission
        db = SessionLocal()
        try:
            order = crud.order.get(db, id=order_id)
            crud.order.update(
                db, db_obj=order, obj_in={"submit_state": "failed"}  # type: ignore
            )

            # send auto-submit failure emails
            send_failed_autosubmit_emails(
                order_obj=order, artifact_name=object_name  # type: ignore
            )
        finally:
            db.close()
    return submission_id


@celery_app.task  # (acks_late=True)
def submit_numerai_model_subtask(order_json: Dict, retry: bool = True) -> Optional[Any]:
    """
    Submit Numerai model subtask

    Args:
        order_json (dict): dict of order information
        retry (bool): whether to retry on failure

    Returns:

    """
    db = SessionLocal()
    try:
        order_id = order_json["id"]
        print(f"Checking artifact submission for order [{order_id}]")

        # Get artifacts
        product = crud.product.get(db=db, id=order_json["product_id"])
        site_globals = crud.globals.update_singleton(db)
        selling_round = site_globals.selling_round  # type: ignore

        artifacts = crud.artifact.get_multi_by_product_round(
            db, product=product, round_tournament=selling_round  # type: ignore
        )

        # No csv artifact
        if (
            not artifacts
            or len(artifacts) == 0
            or len(
                [
                    artifact
                    for artifact in artifacts
                    if artifact.object_name.endswith(".csv")  # type: ignore
                ]
            )
            == 0
        ):
            if site_globals.is_doing_round_rollover:  # Round about to close, finish
                print(
                    f"Submission for order [{order_id}] interrupted due to round closing"
                )
                return None
            # Check again later
            if retry:
                print(
                    f"No csv artifact for order [{order_id}], "
                    f"trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
                )
                celery_app.send_task(
                    "app.worker.submit_numerai_model_subtask",
                    kwargs=dict(order_json=order_json),
                    countdown=settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS,
                )
            else:
                print(f"No csv artifact for order [{order_id}]")
            return None

        # Has csv artifact
        csv_artifact = [
            artifact
            for artifact in artifacts
            if artifact.object_name.endswith(".csv")  # type: ignore
        ][-1]
        bucket = deps.get_gcs_bucket()
        blob = bucket.blob(csv_artifact.object_name)
        if not blob.exists():
            if retry:
                # Check again later
                print(
                    f"Csv artifact for order [{order_id}] not yet uploaded, "
                    f"trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
                )
                celery_app.send_task(
                    "app.worker.submit_numerai_model_subtask",
                    kwargs=dict(order_json=order_json),
                    countdown=settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS,
                )
            else:
                print(f"Csv artifact for order [{order_id}] not yet uploaded")
            return None

        buyer = crud.user.get(db, id=order_json["buyer_id"])

        if buyer:
            print(
                f"Uploading csv artifact {csv_artifact.object_name} for order {order_id}"
            )
            celery_app.send_task(
                "app.worker.upload_numerai_artifact_task",
                kwargs=dict(
                    order_id=order_id,
                    object_name=csv_artifact.object_name,
                    model_id=order_json["submit_model_id"],
                    numerai_api_key_public_id=buyer.numerai_api_key_public_id,
                    numerai_api_key_secret=buyer.numerai_api_key_secret,
                    tournament=product.model.tournament,  # type: ignore
                    version=1,
                ),
            )
    finally:
        db.close()
    return None


@celery_app.task  # (acks_late=True)
def batch_submit_numerai_models_task() -> None:
    """Batch submit Numerai models task"""
    db = SessionLocal()
    try:
        orders = crud.order.get_pending_submission_orders(
            db, round_order=crud.globals.update_singleton(db).selling_round
        )

        print(f"total orders to submit: {len(orders)}")

        group(
            [
                submit_numerai_model_subtask.s(jsonable_encoder(order))
                for order in orders
            ]
        ).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def validate_artifact_upload_task(  # pylint: disable=too-many-branches
    artifact_id: int, skip_if_active: bool = True
) -> None:
    """
    Validate artifact upload task

    Args:
        artifact_id (int): artifact ID
        skip_if_active (bool): whether to skip validation if artifact has already been validated
    """
    db = SessionLocal()
    try:
        artifact = crud.artifact.get(db, id=artifact_id)

        if skip_if_active and artifact and artifact.state == "active":
            print(
                f"Artifact {artifact_id} {artifact.object_name} already validated, skipping"
            )
            return None

        if artifact and artifact.object_name:  # if is file
            bucket = deps.get_gcs_bucket()
            blob = bucket.blob(artifact.object_name)
            if not blob.exists():
                print(
                    f"Artifact {artifact_id} {artifact.object_name} not uploaded, deleting"
                )

                if settings.EMAILS_ENABLED:
                    # Send failed artifact email notification to seller
                    if artifact.product.owner.email:
                        send_failed_artifact_seller_email(
                            email_to=artifact.product.owner.email,
                            username=artifact.product.owner.username,
                            round_tournament=artifact.round_tournament,  # type: ignore
                            product=artifact.product.sku,
                            artifact=artifact.object_name,
                        )

                # crud.artifact.remove(db, id=artifact_id)
                crud.artifact.update(db, db_obj=artifact, obj_in={"state": "failed"})
                return None

            print(
                f"Artifact {artifact_id} {artifact.object_name} is valid, "
                f"searching for orders to upload..."
            )

            selling_round = crud.globals.get_singleton(  # type: ignore
                db=db
            ).selling_round

            # Submit for all confirmed orders with submit_model_id regardless if submitted or not
            # orders = crud.order.get_multi_by_state(
            #     db, state="confirmed", round_order=selling_round  # type: ignore
            # )
            orders = crud.order.get_active_orders(db, round_order=selling_round)
            for order in orders:
                if not order.submit_model_id:
                    continue
                # Disable queue check to always redo queuing
                # if (
                #     order.submit_state == "queued"
                # ):  # already queued for submission, skip
                #     print(f"Order {order.id} already queued for submission, skipped")
                #     continue

                print(
                    f"Uploading csv artifact {artifact.object_name} for order {order.id}"
                )
                if order.submit_model_id and order.product_id == artifact.product_id:
                    celery_app.send_task(
                        "app.worker.upload_numerai_artifact_task",
                        kwargs=dict(
                            order_id=order.id,
                            object_name=artifact.object_name,
                            model_id=order.submit_model_id,
                            numerai_api_key_public_id=order.buyer.numerai_api_key_public_id,
                            numerai_api_key_secret=order.buyer.numerai_api_key_secret,
                            tournament=order.product.model.tournament,
                            version=1,
                        ),
                    )

            # if artifact.state == "pending":  # artifact not yet validated and
            # notified
            print(
                f"Mark artifact {artifact.id} as active and send out email notifications"
            )
            celery_app.send_task(
                "app.worker.send_new_artifact_emails_task",
                kwargs=dict(artifact_id=artifact.id),
            )
            crud.artifact.update(db, db_obj=artifact, obj_in={"state": "active"})

            # mark product as ready
            product = crud.product.get(db, id=artifact.product_id)
            if product:
                if not product.is_ready:
                    crud.product.update(db, db_obj=product, obj_in={"is_ready": True})
    finally:
        db.close()
    return None


@celery_app.task  # (acks_late=True)
def batch_validate_numerai_models_stake_task() -> None:
    """batch validate Numerai models stake task"""
    db = SessionLocal()
    try:
        # orders = crud.order.get_multi_by_state(
        #     db, state="confirmed", round_order=globals.selling_round
        # )
        orders = crud.order.get_active_orders(
            db, round_order=crud.globals.update_singleton(db).selling_round
        )

        print(f"total orders to check for stake limit: {len(orders)}")

        for order in orders:
            if order.mode != "stake_with_limit" or not order.submit_model_id:
                continue
            target_stake = numerai.get_target_stake(
                public_id=order.buyer.numerai_api_key_public_id,  # type: ignore
                secret_key=order.buyer.numerai_api_key_secret,  # type: ignore
                tournament=order.product.model.tournament,  # type: ignore
                model_name=order.submit_model_name,  # type: ignore
            )
            stake_limit = Decimal(order.stake_limit)  # type: ignore
            if target_stake > stake_limit:
                print(
                    f"Order {order.id} model {order.submit_model_name} "
                    f"[user {order.buyer_id}: {order.buyer.username}] "
                    f"exceeded stake limit {target_stake} / {stake_limit}"
                )
                result = numerai.set_target_stake(
                    public_id=order.buyer.numerai_api_key_public_id,  # type: ignore
                    secret_key=order.buyer.numerai_api_key_secret,  # type: ignore
                    tournament=order.product.model.tournament,  # type: ignore
                    model_name=order.submit_model_name,  # type: ignore
                    target_stake_amount=stake_limit,
                )
                print(
                    f"Adjustment result for model {order.submit_model_name}: {result}"
                )
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_stake_snapshots() -> None:
    """Batch update stake snapshots task"""
    db = SessionLocal()
    try:
        # Connect existing stake snapshots
        db.query(StakeSnapshot).filter(StakeSnapshot.model_id.is_(None)).update(
            {
                StakeSnapshot.model_id: select(Model.id)  # type: ignore
                .where(
                    and_(
                        Model.name == StakeSnapshot.name,
                        Model.tournament == StakeSnapshot.tournament,
                    )
                )
                .scalar_subquery()
            },
            synchronize_session=False,
        )
        db.commit()

        # Pull new snapshots
        date_creation = datetime.utcnow()
        active_round = crud.globals.get_singleton(db=db).active_round  # type: ignore
        numerai_models = numerai.get_leaderboard(tournament=8)

        db_models = db.query(Model).filter(Model.tournament == 8).all()
        db_models_dict = {}
        for model in db_models:
            db_models_dict[model.name] = model

        db_stake_snapshots_dict = {}
        for model in numerai_models:
            new_snapshot = StakeSnapshot(
                date_creation=date_creation,
                round_tournament=active_round,
                name=model["username"],
                tournament=8,
                nmr_staked=model["nmrStaked"],
                return_13_weeks=model["return13Weeks"],
                return_52_weeks=model["return52Weeks"],
            )
            if model["username"] in db_models_dict:
                new_snapshot.model_id = db_models_dict[model["username"]].id
            db_stake_snapshots_dict[model["username"]] = new_snapshot
        db.add_all(db_stake_snapshots_dict.values())
        db.commit()

        signals_models = numerai.get_leaderboard(tournament=11)

        db_models = db.query(Model).filter(Model.tournament == 11).all()
        db_models_dict = {}
        for model in db_models:
            db_models_dict[model.name] = model

        db_stake_snapshots_dict = {}
        for model in signals_models:
            new_snapshot = StakeSnapshot(
                date_creation=date_creation,
                round_tournament=active_round,
                name=model["username"],
                tournament=11,
                nmr_staked=model["nmrStaked"],
                return_13_weeks=model["return13Weeks"],
                return_52_weeks=model["return52Weeks"],
            )
            if model["username"] in db_models_dict:
                new_snapshot.model_id = db_models_dict[model["username"]].id
            db_stake_snapshots_dict[model["username"]] = new_snapshot
        db.add_all(db_stake_snapshots_dict.values())
        db.commit()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_delivery_rate() -> None:
    """Batch update delivery rate task"""
    db = SessionLocal()
    try:
        selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore

        users = crud.user.search(
            # type: ignore
            db,
            filters={"numerai_api_key_public_id": ["any"]},
            limit=None,
        )["data"]

        for user in users:
            if not user.products or len(user.products) == 0:
                continue
            for product in user.products:
                # query_filters = [
                #     Order.product_id == product.id,
                #     Order.state == "confirmed",
                # ]
                # query_filter = functools.reduce(and_, query_filters)
                # total_qty_sales = (
                #     db.query(func.sum(Order.quantity)).filter(query_filter).scalar()
                # )
                # product.total_qty_sales = total_qty_sales

                # todo improve query efficiency
                total_qty_sales = 0
                total_qty_delivered = 0
                product_artifacts_rounds = set(
                    [
                        product_artifact.round_tournament
                        for product_artifact in product.artifacts
                        if product_artifact.state != "expired"
                    ]
                )
                query_filters = [
                    Order.product_id == product.id,
                    Order.state == "confirmed",
                    Order.round_order < selling_round,
                ]
                query_filter = functools.reduce(and_, query_filters)
                orders = db.query(Order).filter(query_filter).all()
                if orders and len(orders) > 0:
                    for order in orders:
                        order_artifacts_rounds = set(
                            [
                                order_artifact.round_tournament
                                for order_artifact in order.artifacts
                                if order_artifact.state != "failed"
                            ]
                        )
                        delivered_rounds = product_artifacts_rounds.union(
                            order_artifacts_rounds
                        )
                        if product.category.is_per_round:
                            for tournament_round in range(
                                order.round_order,
                                min(order.round_order + order.quantity, selling_round),
                            ):
                                total_qty_sales += 1
                                if tournament_round in delivered_rounds:
                                    total_qty_delivered += 1
                        else:
                            total_qty_sales += order.quantity
                            if order.round_order in delivered_rounds:
                                total_qty_delivered += order.quantity
                product.total_qty_sales = total_qty_sales
                product.total_qty_delivered = total_qty_delivered

        db.commit()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_polls() -> None:
    """Batch update polls task"""
    db = SessionLocal()
    try:
        date_now = datetime.utcnow()
        expired_polls = db.query(Poll).filter(
            and_(Poll.date_finish <= date_now, Poll.is_finished.is_(False))
        )
        for poll in expired_polls:
            # todo if poll.weight_mode not poll.is_stake_predetermined
            poll.is_finished = True
        db.commit()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_prune_storage() -> None:
    """Batch prune storage task"""
    # prune artifacts
    db = SessionLocal()
    try:
        query_filters = [Category.is_per_round, Artifact.state != "pruned"]
        query_filter = functools.reduce(and_, query_filters)

        subq = (
            db.query(
                Artifact.product_id,
                func.max(Artifact.round_tournament).label("max_round"),
            )
            .group_by(Artifact.product_id)
            .subquery()
        )

        artifacts_to_prune = (
            db.query(Artifact)
            .join(Artifact.product)
            .join(Product.category)
            .join(
                subq,
                and_(
                    Artifact.product_id == subq.c.product_id,
                    Artifact.round_tournament < subq.c.max_round,
                ),
            )
            .filter(query_filter)
            .all()
        )

        print(f"{len(artifacts_to_prune)} artifacts to prune")

        bucket = deps.get_gcs_bucket()
        for artifact in artifacts_to_prune:
            object_name = artifact.object_name
            if object_name:
                try:
                    blob = bucket.blob(object_name)
                    blob.delete()
                except NotFound:
                    pass

            artifact.state = "pruned"
        db.commit()
    finally:
        db.close()

    # prune order artifacts
    db = SessionLocal()
    try:
        order_artifacts_to_prune = (
            db.query(OrderArtifact)
            .filter(OrderArtifact.state == "marked_for_pruning")
            .all()
        )
        print(f"{len(order_artifacts_to_prune)} order artifacts to prune")

        bucket = deps.get_gcs_bucket()
        for order_artifact in order_artifacts_to_prune:
            object_name = order_artifact.object_name
            if object_name:
                try:
                    blob = bucket.blob(object_name)
                    blob.delete()
                except NotFound:
                    pass

            order_artifact.state = "pruned"
        db.commit()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def trigger_webhook_for_product_task(product_id: int, order_id: int = None) -> None:
    """
    Trigger product webhook for new order task

    Args:
        product_id (int): product ID
        order_id (int): order ID
    """
    db = SessionLocal()
    try:
        selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
        product = crud.product.get(db, id=product_id)
        if not product:
            return None
        if not product.webhook:
            return None
        date_str = datetime.now().isoformat()
        response = requests.post(
            product.webhook,
            json={
                "date": date_str,
                "product_id": product.id,
                "product_category": product.category.slug,  # type: ignore
                "product_name": product.name,
                "product_full_name": product.sku,
                "model_id": product.model_id,
                "tournament": product.category.tournament,  # type: ignore
                "order_id": order_id,
                "round_tournament": selling_round,
            },
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            send_failed_webhook_email(
                email_to=product.owner.email,  # type: ignore
                username=product.owner.username,
                date=date_str,
                product=product.sku,
            )
            print(
                f"Webhook for {product.sku} ({product.id}) "
                f"returned an error {response.status_code}"
            )
            return None
        send_succeeded_webhook_email(
            email_to=product.owner.email,  # type: ignore
            username=product.owner.username,
            date=date_str,
            product=product.sku,
        )
        print(f"Webhook for {product.sku} ({product.id}) succeeded")
    finally:
        db.close()
    return None


@celery_app.on_after_configure.connect
def setup_periodic_tasks(  # type: ignore  # pylint: disable=unused-argument
    sender,  # type: ignore
    **kwargs,
) -> None:
    """Setup celery scheduled tasks"""

    print("Setup Cron Tasks")
    sender.conf.beat_schedule = {
        "test_tick": {
            "task": "app.worker.tick",
            "schedule": crontab(day_of_week="wed-sun", hour=0, minute=0),
            "args": (["cron test"]),
        },
        # "batch_update_models": {
        #     "task": "app.worker.batch_update_models_task",
        #     "schedule": crontab(day_of_week="wed-sun", hour=0, minute=0),
        # },
        "batch_update_model_scores": {
            "task": "app.worker.batch_update_model_scores_task",
            "schedule": crontab(day_of_week="tue-sat", hour=14, minute=0),
            "kwargs": dict(retries=10),
        },
        "update_globals_stats_task": {
            "task": "app.worker.update_globals_stats_task",
            "schedule": crontab(hour=0, minute=0),
        },
        "update_active_round": {
            "task": "app.worker.update_active_round",
            "schedule": crontab(day_of_week="sat", hour=18, minute=00),
        },
        "update_round_rollover": {
            "task": "app.worker.update_round_rollover",
            "schedule": crontab(day_of_week="mon", hour=14, minute=00),
        },
        "batch_update_stake_snapshots": {
            "task": "app.worker.batch_update_stake_snapshots",
            "schedule": crontab(day_of_week="mon", hour=14, minute=30),
        },
        "batch_update_delivery_rate": {
            "task": "app.worker.batch_update_delivery_rate",
            "schedule": crontab(day_of_week="mon", hour=14, minute=45),
        },
        "batch_update_polls": {
            "task": "app.worker.batch_update_polls",
            "schedule": crontab(hour=0, minute=0),
        },
        "batch_prune_storage": {
            "task": "app.worker.batch_prune_storage",
            "schedule": crontab(day_of_week="wed", hour=0, minute=0),
        },
        "batch_send_order_artifact_upload_reminder_emails_1": {
            "task": "app.worker.send_order_artifact_upload_reminder_emails_task",
            "schedule": crontab(day_of_week="sun", hour=18, minute=00),
        },
        "batch_send_order_artifact_upload_reminder_emails_2": {
            "task": "app.worker.send_order_artifact_upload_reminder_emails_task",
            "schedule": crontab(day_of_week="mon", hour=12, minute=00),
        },
    }
    sender.add_periodic_task(
        settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
        batch_update_payments_task.s(),
        name=f"batch update payments every {settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS} seconds",
    )
