""" Celery worker tasks """

import functools
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

import pandas as pd
from celery import group
from celery.schedules import crontab
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import NotFound
from raven import Client
from sqlalchemy import and_, func, select

from app import crud
from app.api import deps
from app.api.dependencies import numerai
from app.api.dependencies.commons import on_round_open
from app.api.dependencies.orders import send_order_upload_reminder_emails
from app.core.async_tasks import (
    TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES,
    TASK_BATCH_UPDATE_NUMERAI_MODELS,
    TASK_CHECK_NUMERAI_SUBMISSION,
    TASK_SEND_EMAIL,
    TASK_SEND_NEW_ARTIFACT_EMAILS,
    TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS,
    TASK_TRIGGER_WEBHOOK_FOR_PRODUCT,
    TASK_UPDATE_NUMERAI_MODEL,
    TASK_UPDATE_PAYMENT,
    TASK_UPLOAD_NUMERAI_ARTIFACT,
    TASK_VALIDATE_ARTIFACT_UPLOAD,
    enqueue_pending_payment_updates,
    run_async_task,
)
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal, run_with_db_session
from app.models import (
    Artifact,
    Category,
    Model,
    OrderArtifact,
    Poll,
    Product,
    StakeSnapshot,
)

client_sentry = Client(settings.SENTRY_DSN)


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

    return run_async_task(
        TASK_SEND_EMAIL,
        kwargs=dict(
            email_to=email_to,
            subject_template=subject_template,
            html_template=html_template,
            environment=environment or {},
        ),
    )


@celery_app.task  # (acks_late=True)
def send_new_artifact_emails_task(artifact_id: int) -> None:
    """
    Send new artifact email task

    Args:
        artifact_id (int): artifact id
    """
    return run_async_task(TASK_SEND_NEW_ARTIFACT_EMAILS, args=[artifact_id])


@celery_app.task  # (acks_late=True)
def send_new_order_artifact_emails_task(artifact_id: str) -> None:
    """
    Send new order artifact email task

    Args:
        artifact_id (str): order artifact id
    """
    return run_async_task(TASK_SEND_NEW_ORDER_ARTIFACT_EMAILS, args=[artifact_id])


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
            send_order_upload_reminder_emails(order)
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
    return run_async_task(
        TASK_UPDATE_NUMERAI_MODEL,
        kwargs=dict(user_json=user_json, retries=retries),
    )


@celery_app.task  # (acks_late=True)
def batch_update_models_task() -> None:
    """Batch upload Numerai models task"""
    return run_async_task(TASK_BATCH_UPDATE_NUMERAI_MODELS)


@celery_app.task  # (acks_late=True)
def batch_update_model_scores_task(retries: int = 0) -> None:
    """
    Batch update Numerai models scores task

    Args:
        retries (int): number of tries
    """
    return run_async_task(
        TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES,
        kwargs=dict(retries=retries),
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
    # Get active round info from Numerai
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

    # Get current globals with minimal DB session
    site_globals = run_with_db_session(lambda db: crud.globals.get_singleton(db))

    if open_time <= utc_time <= close_staking_time:
        if site_globals.active_round != active_round_number:  # type: ignore
            # new round opened and active
            print(
                f"UTC time: {utc_time}, round open: {open_time}, "
                f"round close: {close_staking_time}, round: {active_round_number}"
            )
            print(f"Round {active_round_number} opened")

            # Update active round
            run_with_db_session(
                lambda db: crud.globals.update(
                    db,
                    db_obj=crud.globals.get_singleton(db),  # type: ignore
                    obj_in={"active_round": active_round_number},
                )
            )

            # trigger Numerai submissions
            celery_app.send_task("app.worker.batch_submit_numerai_models_task")

            # trigger other actions on round open
            run_with_db_session(lambda db: on_round_open(db))

        if close_staking_time - utc_time <= timedelta(minutes=2):
            # round about to close
            print("Activities freezed due to round rollover")
            # freeze activities
            # crud.globals.update(
            #     db,
            #     db_obj=site_globals,  # type: ignore
            #     obj_in={"is_doing_round_rollover": True},
            # )

            # check order stake
            celery_app.send_task(
                "app.worker.batch_validate_numerai_models_stake_task",
            )
    else:  # current round closed for staking, start selling next round, unfreeze activities
        if (
            site_globals.active_round == active_round_number  # type: ignore
            and site_globals.selling_round == active_round_number + 1  # type: ignore
        ):  # active round already up-to-date
            print("Round already up-to-date, no action")
        else:
            print("Unfreeze activities, rollover completed")
            selling_round = active_round_number + 1

            def update_and_process(db):
                # Update globals
                site_globals_obj = crud.globals.update(
                    db,
                    db_obj=site_globals,  # type: ignore
                    obj_in={
                        "active_round": active_round_number,
                        "selling_round": selling_round,
                        "is_doing_round_rollover": False,
                    },
                )

                # expire old products
                crud.product.bulk_expire(db, current_round=site_globals.selling_round)  # type: ignore

                # mark order artifacts for pruning
                crud.order_artifact.bulk_mark_for_pruning(db, current_round=site_globals.selling_round)  # type: ignore

                # unmark product readiness
                crud.product.bulk_unmark_is_ready(db)

                return site_globals_obj

            # Execute all database operations in a single session
            run_with_db_session(update_and_process)

    # Print current global state with minimal DB session
    current_globals = run_with_db_session(
        lambda db: jsonable_encoder(crud.globals.get_singleton(db))
    )
    print(f"Current global state: {current_globals}")


# @celery_app.task  # (acks_late=True)
# def update_round_rollover() -> None:
#     """Update round rollover task"""
#     db = SessionLocal()
#     try:
#         site_globals = crud.globals.get_singleton(db)
#
#         active_round = numerai.get_numerai_active_round()
#         utc_time = datetime.now(timezone.utc)
#         open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
#         close_staking_time = pd.to_datetime(
#             active_round["closeStakingTime"]
#         ).to_pydatetime()
#         # next_round_open_time = pd.to_datetime(active_round["closeTime"]).to_pydatetime()
#
#         active_round_number = active_round["number"]
#         print(
#             f"UTC time: {utc_time}, round open: {open_time}, "
#             f"round close: {close_staking_time}, round: {active_round_number}"
#         )
#
#         if open_time <= utc_time <= close_staking_time:  # new round opened and active
#             print("Activities freezed due to round rollover")
#             # freeze activities
#             crud.globals.update(
#                 db,
#                 db_obj=site_globals,  # type: ignore
#                 obj_in={"is_doing_round_rollover": True},
#             )
#
#             # check order stake
#             celery_app.send_task(
#                 "app.worker.batch_validate_numerai_models_stake_task",
#             )
#
#             # check again soon
#             celery_app.send_task(
#                 "app.worker.update_round_rollover",
#                 countdown=settings.ROUND_ROLLOVER_POLL_FREQUENCY_SECONDS,
#             )
#         else:  # current round closed for staking, start selling next round, unfreeze activities
#             if (
#                 site_globals.active_round == active_round_number  # type: ignore
#                 and site_globals.selling_round == active_round_number + 5  # type: ignore
#                 # type: ignore
#             ):  # active round already up-to-date
#                 print("Round already up-to-date, no action")
#             else:
#                 print("Unfreeze activities, rollover completed")
#                 selling_round = active_round_number + 5
#                 crud.globals.update(
#                     db,
#                     db_obj=site_globals,  # type: ignore
#                     obj_in={
#                         "active_round": active_round_number,
#                         "selling_round": selling_round,
#                         "is_doing_round_rollover": False,
#                     },
#                 )  # update round number and unfreeze
#                 # expire old products
#                 crud.product.bulk_expire(
#                     db, current_round=site_globals.selling_round  # type: ignore
#                 )
#
#                 # mark order artifacts for pruning
#                 crud.order_artifact.bulk_mark_for_pruning(
#                     db, current_round=site_globals.selling_round  # type: ignore
#                 )
#
#                 # unmark product readiness
#                 crud.product.bulk_unmark_is_ready(db)
#     finally:
#         print(
#             f"Current global state: {jsonable_encoder(crud.globals.get_singleton(db))}"
#         )
#         db.close()


@celery_app.task  # (acks_late=True)
def update_payment_subtask(order_id: int) -> None:
    """
    Update payment subtask

    Args:
        order_id (int): order id
    """
    return run_async_task(TASK_UPDATE_PAYMENT, args=[order_id])


@celery_app.task  # (acks_late=True)
def batch_update_payments_task() -> None:
    """Batch update payments task"""
    total_queued = enqueue_pending_payment_updates()
    print(f"total pending orders: {total_queued}")


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
    return run_async_task(
        TASK_UPLOAD_NUMERAI_ARTIFACT,
        kwargs=dict(
            order_id=order_id,
            object_name=object_name,
            model_id=model_id,
            numerai_api_key_public_id=numerai_api_key_public_id,
            numerai_api_key_secret=numerai_api_key_secret,
            tournament=tournament,
            version=version,
        ),
    )


@celery_app.task  # (acks_late=True)
def submit_numerai_model_subtask(order_json: Dict, retry: bool = True) -> Optional[Any]:
    """
    Submit Numerai model subtask

    Args:
        order_json (dict): dict of order information
        retry (bool): whether to retry on failure

    Returns:

    """
    return run_async_task(
        TASK_CHECK_NUMERAI_SUBMISSION,
        kwargs=dict(order_json=order_json, retry=retry),
    )


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
    return run_async_task(
        TASK_VALIDATE_ARTIFACT_UPLOAD,
        kwargs=dict(artifact_id=artifact_id, skip_if_active=skip_if_active),
    )


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

        # Numerai tournament
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

        # Signal tournament
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

        # Crypto tournament
        # TODO: Check correctness
        crypto_models = numerai.get_leaderboard(tournament=12)

        db_models = db.query(Model).filter(Model.tournament == 12).all()
        db_models_dict = {}
        for model in db_models:
            db_models_dict[model.name] = model

        db_stake_snapshots_dict = {}
        for model in crypto_models:
            new_snapshot = StakeSnapshot(
                date_creation=date_creation,
                round_tournament=active_round,
                name=model["username"],
                tournament=12,
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


@celery_app.task
def batch_update_product_sales_stats() -> None:
    """Batch update product sales stats task"""

    def update_sales_stats(db):
        products = crud.product.get_multi(db=db)
        for product in products:
            if product.model:
                product_sales_stats = crud.product.get_sales_stats(
                    db, product_id=product.id
                )
                product.total_qty_sales = product_sales_stats["total_qty_sales"]
                product.total_qty_sales_filtered = product_sales_stats[
                    "total_qty_sales_filtered"
                ]
                product.total_qty_delivered = product_sales_stats["total_qty_delivered"]
        db.commit()

    run_with_db_session(update_sales_stats)


# @celery_app.task  # (acks_late=True)
# def batch_update_delivery_rate() -> None:
#     """Batch update delivery rate task"""
#     db = SessionLocal()
#     try:
#         selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
#
#         users = crud.user.search(
#             # type: ignore
#             db,
#             filters={"numerai_api_key_public_id": ["any"]},
#             limit=None,
#         )["data"]
#
#         for user in users:
#             if not user.products or len(user.products) == 0:
#                 continue
#             for product in user.products:
#                 # query_filters = [
#                 #     Order.product_id == product.id,
#                 #     Order.state == "confirmed",
#                 # ]
#                 # query_filter = functools.reduce(and_, query_filters)
#                 # total_qty_sales = (
#                 #     db.query(func.sum(Order.quantity)).filter(query_filter).scalar()
#                 # )
#                 # product.total_qty_sales = total_qty_sales
#
#                 # todo improve query efficiency
#                 total_qty_sales = 0
#                 total_qty_delivered = 0
#                 product_artifacts_rounds = set(
#                     [
#                         product_artifact.round_tournament
#                         for product_artifact in product.artifacts
#                         if product_artifact.state != "expired"
#                     ]
#                 )
#                 query_filters = [
#                     Order.product_id == product.id,
#                     Order.state == "confirmed",
#                     Order.round_order < selling_round,
#                 ]
#                 query_filter = functools.reduce(and_, query_filters)
#                 orders = db.query(Order).filter(query_filter).all()
#                 if orders and len(orders) > 0:
#                     for order in orders:
#                         order_artifacts_rounds = set(
#                             [
#                                 order_artifact.round_tournament
#                                 for order_artifact in order.artifacts
#                                 if order_artifact.state != "failed"
#                             ]
#                         )
#                         delivered_rounds = product_artifacts_rounds.union(
#                             order_artifacts_rounds
#                         )
#                         if product.category.is_per_round:
#                             order_rounds = order.rounds
#                             for tournament_round in order_rounds:
#                                 if tournament_round >= selling_round:
#                                     break
#                                 total_qty_sales += 1
#                                 if tournament_round in delivered_rounds:
#                                     total_qty_delivered += 1
#                         else:
#                             total_qty_sales += order.quantity
#                             if order.round_order in delivered_rounds:
#                                 total_qty_delivered += order.quantity
#                 product.total_qty_sales = total_qty_sales
#                 product.total_qty_delivered = total_qty_delivered
#
#         db.commit()
#     finally:
#         db.close()


@celery_app.task  # (acks_late=True)
def batch_update_polls() -> None:
    """Batch update polls task"""

    def update_expired_polls(db):
        date_now = datetime.utcnow()
        expired_polls = db.query(Poll).filter(
            and_(Poll.date_finish <= date_now, Poll.is_finished.is_(False))
        )
        for poll in expired_polls:
            # todo if poll.weight_mode not poll.is_stake_predetermined
            poll.is_finished = True
        db.commit()

    run_with_db_session(update_expired_polls)


@celery_app.task  # (acks_late=True)
def batch_prune_storage() -> None:
    """Batch prune storage task"""
    # prune artifacts
    def get_artifacts_to_prune(db):
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

        # Get a list of object names and IDs
        return [
            {"id": artifact.id, "object_name": artifact.object_name}
            for artifact in artifacts_to_prune
        ]

    # Get artifacts to prune
    artifacts_to_prune = run_with_db_session(get_artifacts_to_prune)
    print(f"{len(artifacts_to_prune)} artifacts to prune")

    # Delete files from GCS bucket
    bucket = deps.get_gcs_bucket()
    for artifact in artifacts_to_prune:
        object_name = artifact["object_name"]
        if object_name:
            try:
                blob = bucket.blob(object_name)
                blob.delete()
            except NotFound:
                pass

    # Mark artifacts as pruned
    def mark_artifacts_pruned(db):
        for artifact_data in artifacts_to_prune:
            artifact = crud.artifact.get(db, id=artifact_data["id"])
            if artifact:
                artifact.state = "pruned"
        db.commit()

    run_with_db_session(mark_artifacts_pruned)

    # prune order artifacts
    def get_order_artifacts_to_prune(db):
        order_artifacts_to_prune = (
            db.query(OrderArtifact)
            .filter(OrderArtifact.state == "marked_for_pruning")
            .all()
        )
        # Get a list of object names and IDs
        return [
            {"id": artifact.id, "object_name": artifact.object_name}
            for artifact in order_artifacts_to_prune
        ]

    # Get order artifacts to prune in a short DB session
    order_artifacts_to_prune = run_with_db_session(get_order_artifacts_to_prune)
    print(f"{len(order_artifacts_to_prune)} order artifacts to prune")

    # Delete files from GCS bucket
    for order_artifact in order_artifacts_to_prune:
        object_name = order_artifact["object_name"]
        if object_name:
            try:
                blob = bucket.blob(object_name)
                blob.delete()
            except NotFound:
                pass

    # Mark order artifacts as pruned
    def mark_order_artifacts_pruned(db):
        for artifact_data in order_artifacts_to_prune:
            order_artifact = crud.order_artifact.get(db, id=artifact_data["id"])
            if order_artifact:
                order_artifact.state = "pruned"
        db.commit()

    run_with_db_session(mark_order_artifacts_pruned)


@celery_app.task  # (acks_late=True)
def trigger_webhook_for_product_task(product_id: int, order_id: int = None) -> None:
    """
    Trigger product webhook for new order task

    Args:
        product_id (int): product ID
        order_id (int): order ID
    """
    return run_async_task(
        TASK_TRIGGER_WEBHOOK_FOR_PRODUCT,
        args=[product_id, order_id],
    )


def is_celery_schedule_owner(owner: str) -> bool:
    """Return whether the given scheduler owner should stay on Celery Beat."""

    return owner == "celery"


def build_beat_schedule() -> Dict[str, Dict[str, Any]]:
    """Build Beat schedules for task families still owned by Celery."""

    beat_schedule = {
        "batch_update_model_scores": {
            "task": "app.worker.batch_update_model_scores_task",
            "schedule": crontab(day_of_week="tue-sat", hour=14, minute=5),
            "kwargs": dict(retries=10),
        },
        "update_active_round": {
            "task": "app.worker.update_active_round",
            "schedule": crontab(),
        },
    }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_GLOBALS_STATS):
        beat_schedule["update_globals_stats_task"] = {
            "task": "app.worker.update_globals_stats_task",
            "schedule": crontab(hour=0, minute=0),
        }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_STAKE_SNAPSHOTS):
        beat_schedule["batch_update_stake_snapshots"] = {
            "task": "app.worker.batch_update_stake_snapshots",
            "schedule": crontab(day_of_week="mon", hour=14, minute=0),
        }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_PRODUCT_SALES_STATS):
        beat_schedule["batch_update_product_sales_stats"] = {
            "task": "app.worker.batch_update_product_sales_stats",
            "schedule": crontab(hour=0, minute=0),
        }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_POLLS):
        beat_schedule["batch_update_polls"] = {
            "task": "app.worker.batch_update_polls",
            "schedule": crontab(hour=0, minute=0),
        }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_PRUNE_STORAGE):
        beat_schedule["batch_prune_storage"] = {
            "task": "app.worker.batch_prune_storage",
            "schedule": crontab(day_of_week="wed", hour=0, minute=0),
        }

    if is_celery_schedule_owner(settings.SCHEDULER_OWNER_ARTIFACT_REMINDERS):
        beat_schedule["batch_send_order_artifact_upload_reminder_emails_1"] = {
            "task": "app.worker.send_order_artifact_upload_reminder_emails_task",
            "schedule": crontab(day_of_week="sun", hour=12, minute=0),
        }
        beat_schedule["batch_send_order_artifact_upload_reminder_emails_2"] = {
            "task": "app.worker.send_order_artifact_upload_reminder_emails_task",
            "schedule": crontab(day_of_week="mon", hour=12, minute=0),
        }

    return beat_schedule


@celery_app.on_after_configure.connect
def setup_periodic_tasks(  # type: ignore  # pylint: disable=unused-argument
    sender,  # type: ignore
    **kwargs,
) -> None:
    """Setup celery scheduled tasks"""

    print("Setup Cron Tasks")
    sender.conf.beat_schedule = build_beat_schedule()
    if settings.ASYNC_OWNER_PAYMENTS == "celery":
        sender.add_periodic_task(
            settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
            batch_update_payments_task.s(),
            name=(
                "batch update payments every "
                f"{settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS} seconds"
            ),
        )
