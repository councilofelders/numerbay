import io
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

import pandas as pd
import requests
from celery import group
from celery.schedules import crontab
from fastapi.encoders import jsonable_encoder
from numerapi import NumerAPI
from raven import Client

from app import crud
from app.api import deps
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.utils import send_email, send_new_artifact_email

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def tick(msg: str) -> str:
    from datetime import datetime

    print(f"Tick! The time is: {datetime.now()}, arg: {msg}")
    sys.stdout.flush()
    import time

    time.sleep(2)
    return msg


@celery_app.task  # (acks_late=True)
def send_email_task(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    send_email(
        email_to=email_to,
        subject_template=subject_template,
        html_template=html_template,
        environment=environment,
    )


@celery_app.task  # (acks_late=True)
def update_model_subtask(user_json: Dict) -> Optional[Any]:
    db = SessionLocal()
    try:
        # Update user info
        crud.user.update_numerai_api(db, user_json)
        # Update user models
        return crud.model.update_model(db, user_json)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_models_task() -> None:
    db = SessionLocal()
    try:
        users = crud.user.search(
            db, filters={"numerai_api_key_public_id": ["any"]}, limit=None  # type: ignore
        )["data"]
        print(f"total: {len(users)}")
        # result = chord([fetch_model_subtask.s(jsonable_encoder(user), 0) for user in users],
        # commit_models_subtask.s(0)).delay()
        group(
            [update_model_subtask.s(jsonable_encoder(user)) for user in users]
        ).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_model_scores_task() -> None:
    pipeline_status = crud.model.get_numerai_pipeline_status(tournament=8)
    if pipeline_status["resolvedAt"]:
        print("Numerai pipeline completed, update model scores...")
        db = SessionLocal()
        try:
            users = crud.user.search(
                db, filters={"numerai_api_key_public_id": ["any"]}, limit=None  # type: ignore
            )["data"]
            print(f"total: {len(users)}")
            # result = chord([fetch_model_subtask.s(jsonable_encoder(user), 0) for user in users],
            # commit_models_subtask.s(0)).delay()
            group(
                [update_model_subtask.s(jsonable_encoder(user)) for user in users]
            ).delay()
        finally:
            db.close()
    else:
        print(
            f"Numerai pipeline not ready, checking again in {settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS}s"
        )
        celery_app.send_task(
            "app.worker.batch_update_model_scores_task",
            countdown=settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS,
        )


@celery_app.task  # (acks_late=True) # todo deprecate old global update to new rollover
def update_globals_task() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.update_singleton(db)
        crud.product.bulk_expire(db, current_round=globals.selling_round)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def update_active_round() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.get_singleton(db)

        active_round = crud.globals.get_numerai_active_round()
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()

        active_round_number = active_round["number"]
        print(
            f"UTC time: {utc_time}, round open: {open_time}, round close: {close_staking_time}, round: {active_round_number}"
        )

        if open_time <= utc_time <= close_staking_time:  # new round opened and active
            print(f"Round {active_round_number} opened")
            # update active round
            crud.globals.update(
                db, db_obj=globals, obj_in={"active_round": active_round_number}  # type: ignore
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
    db = SessionLocal()
    try:
        globals = crud.globals.get_singleton(db)

        active_round = crud.globals.get_numerai_active_round()
        utc_time = datetime.now(timezone.utc)
        open_time = pd.to_datetime(active_round["openTime"]).to_pydatetime()
        close_staking_time = pd.to_datetime(
            active_round["closeStakingTime"]
        ).to_pydatetime()
        # next_round_open_time = pd.to_datetime(active_round["closeTime"]).to_pydatetime()

        active_round_number = active_round["number"]
        print(
            f"UTC time: {utc_time}, round open: {open_time}, round close: {close_staking_time}, round: {active_round_number}"
        )

        if open_time <= utc_time <= close_staking_time:  # new round opened and active
            print("Activities freezed due to round rollover")
            # freeze activities
            crud.globals.update(
                db, db_obj=globals, obj_in={"is_doing_round_rollover": True}  # type: ignore
            )

            # check order stake
            celery_app.send_task("app.worker.batch_validate_numerai_models_stake_task",)

            # check again soon
            celery_app.send_task(
                "app.worker.update_round_rollover",
                countdown=settings.ROUND_ROLLOVER_POLL_FREQUENCY_SECONDS,
            )
        else:  # current round closed for staking, start selling next round, unfreeze activities
            if (
                globals.active_round == active_round_number  # type: ignore
                and globals.selling_round == active_round_number + 1  # type: ignore
                # type: ignore
            ):  # active round already up-to-date
                print("Round already up-to-date, no action")
            else:
                print("Unfreeze activities, rollover completed")
                selling_rouind = active_round_number + 1
                crud.globals.update(
                    db,
                    db_obj=globals,  # type: ignore
                    obj_in={
                        "active_round": active_round_number,
                        "selling_round": selling_rouind,
                        "is_doing_round_rollover": False,
                    },
                )  # update round number and unfreeze
                # expire old products
                crud.product.bulk_expire(db, current_round=globals.selling_round)  # type: ignore
    finally:
        print(
            f"Current global state: {jsonable_encoder(crud.globals.get_singleton(db))}"
        )
        db.close()


@celery_app.task  # (acks_late=True)
def update_payment_subtask(order_json: Dict) -> None:
    db = SessionLocal()
    try:
        # Update order payment
        crud.order.update_payment(db, order_json)
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_update_payments_task() -> None:
    db = SessionLocal()
    try:
        orders = crud.order.get_multi_by_state(db, state="pending")
        print(f"total pending orders: {len(orders)}")
        group(
            [update_payment_subtask.s(jsonable_encoder(order)) for order in orders]
        ).delay()
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def upload_numerai_artifact_task(
    order_id: int,
    object_name: str,
    model_id: str,
    numerai_api_key_public_id: str,
    numerai_api_key_secret: str,
    tournament: int = 8,
    version: int = 1,
) -> Optional[Any]:
    bucket = deps.get_gcs_bucket()
    blob = bucket.blob(object_name)

    # Has csv artifact and uploaded
    url = blob.generate_signed_url(
        expiration=timedelta(minutes=settings.ARTIFACT_DOWNLOAD_URL_EXPIRE_MINUTES),
        # content_type='application/octet-stream',
        bucket_bound_hostname=(
            "https://storage.numerbay.ai"
            if settings.GCP_STORAGE_BUCKET == "storage.numerbay.ai"
            else None
        ),
        method="GET",
        version="v4",
    )

    # Upload URL
    auth_query = """
                        query($filename: String!
                              $tournament: Int!
                              $modelId: String) {
                            submission_upload_auth(filename: $filename
                                                   tournament: $tournament
                                                   modelId: $modelId) {
                                filename
                                url
                            }
                        }
                        """

    arguments = {
        "filename": "predictions.csv",
        "tournament": tournament,
        "modelId": model_id,
    }
    api = NumerAPI(
        public_id=numerai_api_key_public_id, secret_key=numerai_api_key_secret
    )
    submission_auth = api.raw_query(auth_query, arguments, authorization=True)["data"][
        "submission_upload_auth"
    ]
    print(f"Upload url: {submission_auth['url']}")

    # Bridge Upload file
    file_stream = requests.get(url, stream=True)
    # response = requests.put(submission_auth['url'], data=file_stream.iter_content(), stream=True)
    requests.put(
        submission_auth["url"], data=io.BytesIO(file_stream.content), stream=True
    )

    # Create submission
    create_query = """
                            mutation($filename: String!
                                     $tournament: Int!
                                     $version: Int!
                                     $modelId: String
                                     $triggerId: String) {
                                create_submission(filename: $filename
                                                  tournament: $tournament
                                                  version: $version
                                                  modelId: $modelId
                                                  triggerId: $triggerId
                                                  source: "numerapi") {
                                    id
                                }
                            }
                            """
    arguments = {
        "filename": submission_auth["filename"],
        "tournament": tournament,
        "version": version,
        "modelId": model_id,
        "triggerId": None,
    }  # os.getenv('TRIGGER_ID', None)}
    try:
        create = api.raw_query(create_query, arguments, authorization=True)
    except ValueError:  # try again with new data version
        print("Retrying upload with version 2")
        arguments["version"] = 2
        create = api.raw_query(create_query, arguments, authorization=True)
    submission_id = create["data"]["create_submission"]["id"]
    print(f"submission_id: {submission_id}")
    if submission_id:
        # submision successful, mark order submit_state to completed
        db = SessionLocal()
        try:
            order = crud.order.get(db, id=order_id)
            crud.order.update(db, db_obj=order, obj_in={"submit_state": "completed"})  # type: ignore
        finally:
            db.close()
    return submission_id


@celery_app.task  # (acks_late=True)
def submit_numerai_model_subtask(order_json: Dict, retry: bool = True) -> Optional[Any]:
    db = SessionLocal()
    try:
        order_id = order_json["id"]
        print(f"Checking artifact submission for order [{order_id}]")

        # Get artifacts
        product = crud.product.get(db=db, id=order_json["product_id"])
        globals = crud.globals.update_singleton(db)
        selling_round = globals.selling_round  # type: ignore

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
            if globals.is_doing_round_rollover:  # Round about to close, finish
                print(
                    f"Submission for order [{order_id}] interrupted due to round closing"
                )
                return None
            else:  # Check again later
                if retry:
                    print(
                        f"No csv artifact for order [{order_id}], trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
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
            artifact for artifact in artifacts if artifact.object_name.endswith(".csv")  # type: ignore
        ][-1]
        bucket = deps.get_gcs_bucket()
        blob = bucket.blob(csv_artifact.object_name)
        if not blob.exists():
            if retry:
                # Check again later
                print(
                    f"Csv artifact for order [{order_id}] not yet uploaded, trying again in {settings.ARTIFACT_SUBMISSION_POLL_FREQUENCY_SECONDS}s"
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
    db = SessionLocal()
    try:
        globals = crud.globals.update_singleton(db)
        orders = crud.order.get_pending_submission_orders(
            db, round_order=globals.selling_round
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
def validate_artifact_upload_task(artifact_id: int) -> None:
    db = SessionLocal()
    try:
        artifact = crud.artifact.get(db, id=artifact_id)
        if artifact and artifact.object_name:
            bucket = deps.get_gcs_bucket()
            blob = bucket.blob(artifact.object_name)
            if not blob.exists():
                print(
                    f"Artifact {artifact_id} {artifact.object_name} not uploaded, deleting"
                )
                crud.artifact.remove(db, id=artifact_id)
                return None

            selling_round = crud.globals.get_singleton(db=db).selling_round  # type: ignore
            orders = crud.order.get_pending_submission_orders(
                db, round_order=selling_round
            )
            for order in orders:
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

            if settings.EMAILS_ENABLED:
                orders = crud.order.get_multi_by_state(
                    db, state="confirmed", round_order=selling_round
                )
                for order in orders:
                    if order.product_id == artifact.product_id:
                        # Send new artifact email notifications to buyers
                        if order.buyer.email:
                            send_new_artifact_email(
                                email_to=order.buyer.email,
                                username=order.buyer.username,
                                round_order=order.round_order,
                                product=order.product.sku,
                                order_id=order.id,
                                artifact=artifact.object_name,
                            )
    finally:
        db.close()


@celery_app.task  # (acks_late=True)
def batch_validate_numerai_models_stake_task() -> None:
    db = SessionLocal()
    try:
        globals = crud.globals.update_singleton(db)
        orders = crud.order.get_multi_by_state(
            db, state="confirmed", round_order=globals.selling_round
        )

        print(f"total orders to check for stake limit: {len(orders)}")

        for order in orders:
            if order.mode != "stake_with_limit" or not order.submit_model_id:
                continue
            target_stake = crud.model.get_target_stake(
                public_id=order.buyer.numerai_api_key_public_id,  # type: ignore
                secret_key=order.buyer.numerai_api_key_secret,  # type: ignore
                tournament=order.product.model.tournament,  # type: ignore
                model_name=order.submit_model_name,  # type: ignore
            )
            stake_limit = Decimal(order.stake_limit)  # type: ignore
            if target_stake > stake_limit:
                print(
                    f"Order {order.id} model {order.submit_model_name} [user {order.buyer_id}: {order.buyer.username}] exceeded stake limit {target_stake} / {stake_limit}"
                )
                result = crud.model.set_target_stake(
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


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:  # type: ignore
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
        },
        # "update_globals_task": {
        #     "task": "app.worker.update_globals_task",
        #     "schedule": crontab(day_of_week="sat", hour=18, minute=5),
        # },
        "update_active_round": {
            "task": "app.worker.update_active_round",
            "schedule": crontab(day_of_week="sat", hour=18, minute=00),
        },
        "update_round_rollover": {
            "task": "app.worker.update_round_rollover",
            "schedule": crontab(day_of_week="mon", hour=14, minute=00),
        },
    }
    sender.add_periodic_task(
        settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS,
        batch_update_payments_task.s(),
        name=f"batch update payments every {settings.ORDER_PAYMENT_POLL_FREQUENCY_SECONDS} seconds",
    )
