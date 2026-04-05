import base64
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.core import async_tasks


def test_enqueue_async_task_uses_celery_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_NOTIFICATIONS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_send_email(
        email_to="buyer@example.com",
        subject_template="Subject",
        html_template="<p>body</p>",
        environment={"username": "buyer"},
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.send_email_task",
            {
                "args": [],
                "kwargs": {
                    "email_to": "buyer@example.com",
                    "subject_template": "Subject",
                    "html_template": "<p>body</p>",
                    "environment": {"username": "buyer"},
                },
            },
        )
    ]


def test_enqueue_batch_update_numerai_models_uses_ops_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_OPS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_batch_update_numerai_models()

    assert result == "celery-task"
    assert calls == [("app.worker.batch_update_models_task", {"args": [], "kwargs": {}})]


def test_enqueue_batch_update_numerai_model_scores_uses_ops_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_OPS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_batch_update_numerai_model_scores(
        retries=3,
        delay_seconds=30,
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.batch_update_model_scores_task",
            {"args": [], "kwargs": {"retries": 3}, "countdown": 30},
        )
    ]


def test_enqueue_update_active_round_uses_ops_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_OPS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_update_active_round(schedule_slot="202604050901")

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.update_active_round",
            {"args": [], "kwargs": {"schedule_slot": "202604050901"}},
        )
    ]


def test_enqueue_validate_numerai_models_stake_uses_ops_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_OPS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_validate_numerai_models_stake(
        dedupe_key="validate-stake-round-1234-slot-202604050901",
        delay_seconds=5,
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.batch_validate_numerai_models_stake_task",
            {"args": [], "kwargs": {}, "countdown": 5},
        )
    ]


def test_enqueue_async_task_uses_cloud_tasks(monkeypatch) -> None:
    captured = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self):
            return {"name": "task-created"}

    class FakeSession:
        def post(self, url, json):
            captured["url"] = url
            captured["json"] = json
            return FakeResponse()

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_NOTIFICATIONS", "gcp")
    monkeypatch.setattr(
        async_tasks.settings,
        "ASYNC_WORKER_DISPATCH_URL",
        "https://worker.example.com/backend-api/v1/internal/tasks/dispatch",
    )
    monkeypatch.setattr(async_tasks.settings, "ASYNC_WORKER_DISPATCH_TOKEN", "secret")
    monkeypatch.setattr(
        async_tasks.settings,
        "ASYNC_WORKER_SERVICE_ACCOUNT_EMAIL",
        "worker-invoker@numerbay.iam.gserviceaccount.com",
    )
    monkeypatch.setattr(async_tasks.settings, "GCP_PROJECT", "numerbay")
    monkeypatch.setattr(async_tasks.settings, "GCP_TASKS_LOCATION", "us-central1")
    monkeypatch.setattr(
        async_tasks.settings, "GCP_TASKS_QUEUE_NOTIFICATIONS", "notifications"
    )
    monkeypatch.setattr(async_tasks.settings, "GCP_SERVICE_ACCOUNT_INFO", "{}")
    monkeypatch.setattr(async_tasks, "_get_cloud_tasks_session", lambda: FakeSession())

    result = async_tasks.enqueue_send_email(
        email_to="buyer@example.com",
        subject_template="Subject",
        html_template="<p>body</p>",
        environment={"username": "buyer"},
    )

    assert result == {"name": "task-created"}
    assert (
        captured["url"]
        == "https://cloudtasks.googleapis.com/v2/projects/numerbay/locations/us-central1/queues/notifications/tasks"
    )
    http_request = captured["json"]["task"]["httpRequest"]
    assert http_request["headers"]["X-Internal-Task-Token"] == "secret"
    assert http_request["oidcToken"]["serviceAccountEmail"] == (
        "worker-invoker@numerbay.iam.gserviceaccount.com"
    )

    payload = json.loads(base64.b64decode(http_request["body"]).decode("utf-8"))
    assert payload == {
        "task": async_tasks.TASK_SEND_EMAIL,
        "args": [],
        "kwargs": {
            "email_to": "buyer@example.com",
            "subject_template": "Subject",
            "html_template": "<p>body</p>",
            "environment": {"username": "buyer"},
        },
    }


def test_enqueue_update_payment_uses_poll_slot_dedupe(monkeypatch) -> None:
    captured = {}

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_PAYMENTS", "gcp")
    monkeypatch.setattr(
        async_tasks,
        "_enqueue_cloud_task",
        lambda **kwargs: captured.update(kwargs) or {"name": "task-created"},
    )

    result = async_tasks.enqueue_update_payment(42, poll_slot="202604041305")

    assert result == {"name": "task-created"}
    assert captured["kwargs"] == {"poll_slot": "202604041305"}
    assert captured["dedupe_key"] == "order-42-slot-202604041305"


def test_enqueue_validate_artifact_upload_uses_submissions_owner(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_SUBMISSIONS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_validate_artifact_upload(
        12,
        skip_if_active=False,
        delay_seconds=30,
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.validate_artifact_upload_task",
            {
                "args": [],
                "kwargs": {"artifact_id": 12, "skip_if_active": False},
                "countdown": 30,
            },
        )
    ]


def test_enqueue_update_numerai_model_uses_ops_owner(monkeypatch) -> None:
    calls = []
    user_json = {"username": "alice"}

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_OPS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_update_numerai_model(
        user_json,
        retries=5,
        delay_seconds=12,
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.update_model_subtask",
            {
                "args": [],
                "kwargs": {"user_json": user_json, "retries": 5},
                "countdown": 12,
            },
        )
    ]


def test_enqueue_check_numerai_submission_uses_submissions_owner(monkeypatch) -> None:
    calls = []
    order_json = {"id": 7, "submit_model_id": "model-1"}

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_SUBMISSIONS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_check_numerai_submission(
        order_json,
        retry=False,
        delay_seconds=15,
    )

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.submit_numerai_model_subtask",
            {
                "args": [],
                "kwargs": {"order_json": order_json, "retry": False},
                "countdown": 15,
            },
        )
    ]


def test_enqueue_batch_submit_numerai_models_uses_submissions_owner(
    monkeypatch,
) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_SUBMISSIONS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_batch_submit_numerai_models()

    assert result == "celery-task"
    assert calls == [
        ("app.worker.batch_submit_numerai_models_task", {"args": [], "kwargs": {}})
    ]


def test_enqueue_send_new_order_artifact_emails_uses_notifications_owner(
    monkeypatch,
) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_NOTIFICATIONS", "celery")
    monkeypatch.setattr(
        async_tasks.celery_app,
        "send_task",
        lambda name, **kwargs: calls.append((name, kwargs)) or "celery-task",
    )

    result = async_tasks.enqueue_send_new_order_artifact_emails("artifact-123")

    assert result == "celery-task"
    assert calls == [
        (
            "app.worker.send_new_order_artifact_emails_task",
            {"args": ["artifact-123"], "kwargs": {}},
        )
    ]


def test_enqueue_async_task_requires_dispatch_token(monkeypatch) -> None:
    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_NOTIFICATIONS", "gcp")
    monkeypatch.setattr(
        async_tasks.settings,
        "ASYNC_WORKER_DISPATCH_URL",
        "https://worker.example.com/backend-api/v1/internal/tasks/dispatch",
    )
    monkeypatch.setattr(async_tasks.settings, "ASYNC_WORKER_DISPATCH_TOKEN", None)
    monkeypatch.setattr(async_tasks.settings, "GCP_SERVICE_ACCOUNT_INFO", "{}")

    try:
        async_tasks.enqueue_send_email(
            email_to="buyer@example.com",
            subject_template="Subject",
            html_template="<p>body</p>",
        )
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "ASYNC_WORKER_DISPATCH_TOKEN" in str(exc)


def test_enqueue_pending_payment_updates_uses_shared_poll_slot(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks, "_get_pending_order_ids", lambda: [10, 20])
    monkeypatch.setattr(
        async_tasks,
        "enqueue_update_payment",
        lambda order_id, delay_seconds=None, poll_slot=None: calls.append(
            (order_id, delay_seconds, poll_slot)
        ),
    )

    total = async_tasks.enqueue_pending_payment_updates(poll_slot="202604041305")

    assert total == 2
    assert calls == [
        (10, None, "202604041305"),
        (20, None, "202604041305"),
    ]


def test_enqueue_pending_submission_checks_seeds_all_pending_orders(monkeypatch) -> None:
    calls = []
    pending_orders = [{"id": 1}, {"id": 2}]

    monkeypatch.setattr(
        async_tasks,
        "_get_pending_submission_orders_json",
        lambda: pending_orders,
    )
    monkeypatch.setattr(
        async_tasks,
        "enqueue_check_numerai_submission",
        lambda order_json, retry=True, delay_seconds=None: calls.append(
            (order_json, retry, delay_seconds)
        ),
    )

    total = async_tasks.enqueue_pending_submission_checks()

    assert total == 2
    assert calls == [
        ({"id": 1}, True, None),
        ({"id": 2}, True, None),
    ]


def test_run_batch_submit_numerai_models_seeds_all_pending_orders(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(
        async_tasks,
        "enqueue_pending_submission_checks",
        lambda: calls.append("seed") or 3,
    )

    async_tasks.run_async_task(async_tasks.TASK_BATCH_SUBMIT_NUMERAI_MODELS)

    assert calls == ["seed"]


def test_run_update_payment_does_not_reschedule_pending_orders(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_PAYMENTS", "gcp")
    monkeypatch.setattr(async_tasks, "_run_update_payment_in_db", lambda order_id: None)
    monkeypatch.setattr(
        async_tasks,
        "enqueue_update_payment",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    async_tasks.run_async_task(
        async_tasks.TASK_UPDATE_PAYMENT,
        args=[42],
        kwargs={"poll_slot": "202604041305"},
    )

    assert calls == []


def test_run_batch_update_numerai_models_fans_out_with_stagger(monkeypatch) -> None:
    calls = []
    users = [{"username": "alice"}, {"username": "bob"}]

    monkeypatch.setattr(
        async_tasks,
        "enqueue_update_numerai_model",
        lambda user_json, retries=0, delay_seconds=None: calls.append(
            (user_json, retries, delay_seconds)
        ),
    )

    from app import crud
    from app.db import session

    monkeypatch.setattr(
        crud.user,
        "search",
        lambda db, filters, limit=None: {"data": users},
    )
    monkeypatch.setattr(session, "run_with_db_session", lambda fn: fn(None))

    async_tasks.run_async_task(async_tasks.TASK_BATCH_UPDATE_NUMERAI_MODELS)

    assert calls == [
        ({"username": "alice"}, 10, 0),
        ({"username": "bob"}, 10, 0),
    ]


def test_run_batch_update_numerai_model_scores_requeues_until_ready(monkeypatch) -> None:
    calls = []

    from app.api.dependencies import numerai

    monkeypatch.setattr(
        numerai,
        "get_numerai_pipeline_status",
        lambda tournament: {"isScoringDay": True, "resolvedAt": None},
    )
    monkeypatch.setattr(
        async_tasks,
        "enqueue_batch_update_numerai_model_scores",
        lambda retries=0, delay_seconds=None: calls.append((retries, delay_seconds)),
    )

    async_tasks.run_async_task(
        async_tasks.TASK_BATCH_UPDATE_NUMERAI_MODEL_SCORES,
        kwargs={"retries": 4},
    )

    assert calls == [(4, async_tasks.settings.NUMERAI_PIPELINE_POLL_FREQUENCY_SECONDS)]


def test_run_update_active_round_on_round_open_seeds_submissions(monkeypatch) -> None:
    calls = []
    now = datetime.now(timezone.utc)
    site_globals = SimpleNamespace(active_round=1238, selling_round=1239)

    from app import crud
    from app.api.dependencies import commons, numerai
    from app.db import session

    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda: {
            "openTime": (now - timedelta(minutes=30)).isoformat().replace(
                "+00:00", "Z"
            ),
            "closeStakingTime": (now + timedelta(minutes=30)).isoformat().replace(
                "+00:00", "Z"
            ),
            "number": 1239,
        },
    )
    monkeypatch.setattr(
        session,
        "run_with_db_session",
        lambda fn: fn("db-session"),
    )
    monkeypatch.setattr(crud.globals, "get_singleton", lambda db: site_globals)
    monkeypatch.setattr(
        crud.globals,
        "update",
        lambda db, db_obj, obj_in: calls.append(("update-globals", obj_in)) or site_globals,
    )
    monkeypatch.setattr(
        async_tasks,
        "enqueue_batch_submit_numerai_models",
        lambda: calls.append(("enqueue-submissions", None)) or {"name": "task"},
    )
    monkeypatch.setattr(
        commons,
        "on_round_open",
        lambda db: calls.append(("on-round-open", db)),
    )

    async_tasks.run_async_task(
        async_tasks.TASK_UPDATE_ACTIVE_ROUND,
        kwargs={"schedule_slot": "202604050901"},
    )

    assert calls[:3] == [
        ("update-globals", {"active_round": 1239}),
        ("enqueue-submissions", None),
        ("on-round-open", "db-session"),
    ]


def test_run_update_active_round_near_close_enqueues_stake_validation(
    monkeypatch,
) -> None:
    calls = []
    now = datetime.now(timezone.utc)
    site_globals = SimpleNamespace(active_round=1239, selling_round=1239)

    from app import crud
    from app.api.dependencies import numerai
    from app.db import session

    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda: {
            "openTime": (now - timedelta(minutes=30)).isoformat().replace(
                "+00:00", "Z"
            ),
            "closeStakingTime": (now + timedelta(minutes=1)).isoformat().replace(
                "+00:00", "Z"
            ),
            "number": 1239,
        },
    )
    monkeypatch.setattr(
        session,
        "run_with_db_session",
        lambda fn: fn("db-session"),
    )
    monkeypatch.setattr(crud.globals, "get_singleton", lambda db: site_globals)
    monkeypatch.setattr(
        async_tasks,
        "enqueue_validate_numerai_models_stake",
        lambda dedupe_key=None, delay_seconds=None: calls.append(
            (dedupe_key, delay_seconds)
        ),
    )

    async_tasks.run_async_task(
        async_tasks.TASK_UPDATE_ACTIVE_ROUND,
        kwargs={"schedule_slot": "202604050901"},
    )

    assert calls == [("validate-stake-round-1239-slot-202604050901", None)]


def test_send_failed_autosubmit_emails_in_db_reloads_order(monkeypatch) -> None:
    captured = []
    fake_order = SimpleNamespace(id=7)

    from app import crud
    from app.api.dependencies import orders
    from app.db import session

    monkeypatch.setattr(
        crud.order,
        "get",
        lambda db, id: fake_order if id == 7 else None,
    )
    monkeypatch.setattr(
        orders,
        "send_failed_autosubmit_emails",
        lambda order_obj, artifact_name: captured.append((order_obj, artifact_name)),
    )
    monkeypatch.setattr(
        session,
        "run_with_db_session",
        lambda fn: fn("db-session"),
    )

    async_tasks._send_failed_autosubmit_emails_in_db(7, "artifact.csv")

    assert captured == [(fake_order, "artifact.csv")]
