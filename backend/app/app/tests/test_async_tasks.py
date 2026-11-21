import base64
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from app.core import async_tasks


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


def test_enqueue_validate_artifact_upload_uses_submissions_queue(monkeypatch) -> None:
    captured = {}

    monkeypatch.setattr(
        async_tasks,
        "_enqueue_cloud_task",
        lambda **kwargs: captured.update(kwargs) or {"name": "task-created"},
    )

    result = async_tasks.enqueue_validate_artifact_upload(
        12,
        skip_if_active=False,
        delay_seconds=30,
    )

    assert result == {"name": "task-created"}
    assert captured["task_name"] == async_tasks.TASK_VALIDATE_ARTIFACT_UPLOAD
    assert captured["queue_name"] == async_tasks.settings.GCP_TASKS_QUEUE_SUBMISSIONS
    assert captured["kwargs"] == {"artifact_id": 12, "skip_if_active": False}
    assert captured["delay_seconds"] == 30


def test_enqueue_check_numerai_submission_uses_submissions_queue(monkeypatch) -> None:
    captured = {}
    order_json = {"id": 7, "submit_model_id": "model-1"}

    monkeypatch.setattr(
        async_tasks,
        "_enqueue_cloud_task",
        lambda **kwargs: captured.update(kwargs) or {"name": "task-created"},
    )

    result = async_tasks.enqueue_check_numerai_submission(
        order_json,
        retry=False,
        delay_seconds=15,
    )

    assert result == {"name": "task-created"}
    assert captured["task_name"] == async_tasks.TASK_CHECK_NUMERAI_SUBMISSION
    assert captured["queue_name"] == async_tasks.settings.GCP_TASKS_QUEUE_SUBMISSIONS
    assert captured["kwargs"] == {"order_json": order_json, "retry": False}
    assert captured["delay_seconds"] == 15


def test_enqueue_update_payment_uses_poll_slot_dedupe(monkeypatch) -> None:
    captured = {}
    monkeypatch.setattr(
        async_tasks,
        "_enqueue_cloud_task",
        lambda **kwargs: captured.update(kwargs) or {"name": "task-created"},
    )

    result = async_tasks.enqueue_update_payment(42, poll_slot="202604041305")

    assert result == {"name": "task-created"}
    assert captured["kwargs"] == {"poll_slot": "202604041305"}
    assert captured["dedupe_key"] == "order-42-slot-202604041305"


def test_enqueue_async_task_requires_dispatch_token(monkeypatch) -> None:
    monkeypatch.setattr(
        async_tasks.settings,
        "ASYNC_WORKER_DISPATCH_URL",
        "https://worker.example.com/backend-api/v1/internal/tasks/dispatch",
    )
    monkeypatch.setattr(async_tasks.settings, "ASYNC_WORKER_DISPATCH_TOKEN", None)

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


def test_enqueue_pending_submission_checks_seeds_all_pending_orders(
    monkeypatch,
) -> None:
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
    users = [SimpleNamespace(id=1), SimpleNamespace(id=2)]

    monkeypatch.setattr(
        async_tasks,
        "enqueue_update_numerai_model",
        lambda user_id, retries=0, delay_seconds=None: calls.append(
            (user_id, retries, delay_seconds)
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
        (1, 10, 0),
        (2, 10, 0),
    ]


def test_run_batch_update_numerai_model_scores_requeues_until_ready(
    monkeypatch,
) -> None:
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
    site_globals = SimpleNamespace(
        active_round=1238,
        selling_round=1239,
        last_round_open_processed=None,
    )
    fake_db = SimpleNamespace(
        add=lambda obj: None,
        flush=lambda: None,
        commit=lambda: None,
    )

    from app import crud
    from app.api.dependencies import commons, numerai
    from app.db import session

    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda: {
            "openTime": (now - timedelta(minutes=30))
            .isoformat()
            .replace("+00:00", "Z"),
            "closeStakingTime": (now + timedelta(minutes=30))
            .isoformat()
            .replace("+00:00", "Z"),
            "number": 1239,
        },
    )
    monkeypatch.setattr(
        session,
        "run_with_db_session",
        lambda fn: fn(fake_db),
    )
    monkeypatch.setattr(crud.globals, "get_singleton", lambda db: site_globals)
    monkeypatch.setattr(
        async_tasks,
        "_get_locked_globals",
        lambda db, globals_model: site_globals,
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

    assert calls[:2] == [
        ("enqueue-submissions", None),
        ("on-round-open", fake_db),
    ]
    assert site_globals.active_round == 1239
    assert site_globals.selling_round == 1239
    assert site_globals.last_round_open_processed == 1239


def test_run_update_active_round_catches_up_unprocessed_open_round(
    monkeypatch,
) -> None:
    calls = []
    now = datetime.now(timezone.utc)
    site_globals = SimpleNamespace(
        active_round=1239,
        selling_round=1239,
        last_round_open_processed=None,
    )
    fake_db = SimpleNamespace(
        add=lambda obj: None,
        flush=lambda: None,
        commit=lambda: None,
    )

    from app import crud
    from app.api.dependencies import commons, numerai
    from app.db import session

    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda: {
            "openTime": (now - timedelta(minutes=30))
            .isoformat()
            .replace("+00:00", "Z"),
            "closeStakingTime": (now + timedelta(minutes=30))
            .isoformat()
            .replace("+00:00", "Z"),
            "number": 1239,
        },
    )
    monkeypatch.setattr(
        session,
        "run_with_db_session",
        lambda fn: fn(fake_db),
    )
    monkeypatch.setattr(crud.globals, "get_singleton", lambda db: site_globals)
    monkeypatch.setattr(
        async_tasks,
        "_get_locked_globals",
        lambda db, globals_model: site_globals,
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

    assert calls[:2] == [
        ("enqueue-submissions", None),
        ("on-round-open", fake_db),
    ]
    assert site_globals.last_round_open_processed == 1239


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


def _fake_order(order_id, product_id, sku, tournament, **kw):
    return SimpleNamespace(
        id=order_id,
        product_id=product_id,
        round_order=kw.get("round_order", 1400),
        buyer_public_key=kw.get("buyer_public_key"),
        mode=kw.get("mode", "file"),
        submit_model_id=kw.get("submit_model_id"),
        submit_state=kw.get("submit_state"),
        last_submit_round=kw.get("last_submit_round"),
        artifacts=kw.get("artifacts", []),
        buyer=SimpleNamespace(email=f"b{order_id}@ex.com", username=f"b{order_id}"),
        product=SimpleNamespace(
            id=product_id,
            sku=sku,
            category=SimpleNamespace(
                is_per_round=kw.get("is_per_round", True), tournament=tournament
            ),
            owner=SimpleNamespace(
                email=f"s{product_id}@ex.com", username=f"s{product_id}"
            ),
        ),
    )


def _setup_round_close(monkeypatch, orders, *, selling_round=1403):
    now = datetime(2026, 11, 20, 14, 30, tzinfo=timezone.utc)
    site_globals = SimpleNamespace(
        active_round=1403,
        selling_round=selling_round,
        is_doing_round_rollover=False,
        last_round_close_processed=1402,
    )
    ops, sent = [], []

    from app import crud, utils
    from app.api.dependencies import numerai
    from app.db import session

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return now

    def fake_claim(db, round_number, round_closed):
        if site_globals.last_round_close_processed == round_number:
            return False
        site_globals.active_round = round_number
        site_globals.selling_round = round_number + 1
        site_globals.last_round_close_processed = round_number
        return True

    fake_db = SimpleNamespace()
    monkeypatch.setattr(async_tasks, "datetime", FakeDateTime)
    monkeypatch.setattr(async_tasks.settings, "EMAILS_ENABLED", True)
    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda tournament=8: {
            "number": 1404 if tournament == 11 else 1403,
            "openTime": "2026-11-20T12:00:00Z",
            "closeStakingTime": (
                "2026-11-20T14:15:00Z" if tournament == 8 else "2026-11-20T13:05:00Z"
            ),
        },
    )
    monkeypatch.setattr(session, "run_with_db_session", lambda fn: fn(fake_db))
    monkeypatch.setattr(crud.globals, "get_singleton", lambda db: site_globals)
    monkeypatch.setattr(async_tasks, "_claim_round_rollover", fake_claim)
    monkeypatch.setattr(crud.order, "get_active_orders", lambda db, round_order: orders)
    monkeypatch.setattr(
        crud.artifact,
        "get_multi_by_product_round",
        lambda db, product, round_tournament: (
            ops.append(f"check-{product.id}")
            or ([SimpleNamespace(state="active")] if product.id == 11 else [])
        ),
    )
    monkeypatch.setattr(crud.product, "bulk_expire", lambda db, current_round: None)
    monkeypatch.setattr(
        crud.order_artifact,
        "bulk_mark_for_pruning",
        lambda db, current_round: ops.append("prune"),
    )
    monkeypatch.setattr(crud.product, "bulk_unmark_is_ready", lambda db: None)
    monkeypatch.setattr(
        utils,
        "send_missed_upload_email",
        lambda **kw: sent.append({**kw, "after_cleanup": "prune" in ops}),
    )
    return site_globals, ops, sent


def test_run_update_active_round_on_close_notifies_missed_orders(monkeypatch) -> None:
    orders = [
        _fake_order(
            101, 10, "crypto-a", 12, submit_model_id="m1", last_submit_round=1402
        ),
        _fake_order(102, 10, "crypto-a", 12, submit_model_id="m2"),
        _fake_order(103, 11, "classic-ok", 8),
        _fake_order(
            104,
            12,
            "classic-enc",
            8,
            buyer_public_key="pk",
            submit_model_id="m4",
            artifacts=[
                SimpleNamespace(
                    round_tournament=1403, state="active", is_numerai_direct=False
                )
            ],
        ),
        _fake_order(
            105,
            13,
            "classic-fail",
            8,
            buyer_public_key="pk",
            submit_model_id="m5",
            artifacts=[
                SimpleNamespace(
                    round_tournament=1403, state="active", is_numerai_direct=False
                ),
                SimpleNamespace(
                    round_tournament=1403, state="failed", is_numerai_direct=True
                ),
            ],
        ),
        _fake_order(
            106,
            14,
            "classic-race-ok",
            8,
            buyer_public_key="pk",
            submit_model_id="m6",
            submit_state="completed",
            last_submit_round=1403,
            artifacts=[
                SimpleNamespace(
                    round_tournament=1403, state="active", is_numerai_direct=False
                )
            ],
        ),
        _fake_order(107, 15, "model-static", 8, is_per_round=False),
        _fake_order(108, 16, "signals-moved", 11),
    ]
    site_globals, ops, sent = _setup_round_close(monkeypatch, orders)

    async_tasks.run_async_task(async_tasks.TASK_UPDATE_ACTIVE_ROUND)

    assert ops[-1] == "prune" and "check-10" in ops
    assert site_globals.last_round_close_processed == 1403
    assert all(e["after_cleanup"] for e in sent)
    assert [
        (
            e["email_to"],
            e["order_ids"],
            e["close_staking_time"],
            e.get("is_seller", False),
        )
        for e in sent
    ] == [
        ("b101@ex.com", "101", "2026-11-20 13:05 UTC", False),
        ("b102@ex.com", "102", "2026-11-20 13:05 UTC", False),
        ("b104@ex.com", "104", "2026-11-20 14:15 UTC", False),
        ("b108@ex.com", "108", None, False),
        ("s10@ex.com", "101, 102", "2026-11-20 13:05 UTC", True),
        ("s12@ex.com", "104", "2026-11-20 14:15 UTC", True),
        ("s16@ex.com", "108", None, True),
    ]

    sent.clear()
    async_tasks.run_async_task(async_tasks.TASK_UPDATE_ACTIVE_ROUND)
    assert sent == []


def test_run_update_active_round_on_close_catches_up_and_survives_cleanup_error(
    monkeypatch,
) -> None:
    from app import crud

    orders = [_fake_order(101, 10, "crypto-a", 12)]
    site_globals, ops, sent = _setup_round_close(
        monkeypatch, orders, selling_round=1404
    )

    async_tasks.run_async_task(async_tasks.TASK_UPDATE_ACTIVE_ROUND)
    assert (
        site_globals.last_round_close_processed == 1403
        and ops[-1] == "prune"
        and len(sent) == 2
    )

    sent.clear()
    site_globals.last_round_close_processed = 1402
    monkeypatch.setattr(
        crud.product,
        "bulk_expire",
        lambda db, current_round: (_ for _ in ()).throw(RuntimeError("cleanup boom")),
    )
    with pytest.raises(RuntimeError):
        async_tasks.run_async_task(async_tasks.TASK_UPDATE_ACTIVE_ROUND)
    assert site_globals.last_round_close_processed == 1403 and len(sent) == 2


def test_run_update_active_round_on_close_isolates_collection_error(
    monkeypatch,
) -> None:
    site_globals, ops, sent = _setup_round_close(monkeypatch, [])
    monkeypatch.setattr(
        async_tasks,
        "_collect_missed_orders_for_round",
        lambda db, round_tournament: (_ for _ in ()).throw(RuntimeError("query boom")),
    )

    async_tasks.run_async_task(async_tasks.TASK_UPDATE_ACTIVE_ROUND)

    assert site_globals.selling_round == 1404
    assert site_globals.last_round_close_processed == 1403
    assert ops[-1] == "prune"
    assert sent == []


def test_send_order_artifact_upload_reminder_filters_by_round_and_passes_utc(
    monkeypatch,
) -> None:
    reminded = []
    from app import crud
    from app.api.dependencies import numerai
    from app.api.dependencies import orders as order_deps
    from app.db import session

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 11, 20, 12, 30, tzinfo=timezone.utc)

    orders = [
        _fake_order(
            201,
            10,
            "crypto-a",
            12,
            round_order=1400,
            buyer_public_key="pk",
            artifacts=[
                SimpleNamespace(
                    state="active", is_numerai_direct=False, round_tournament=1402
                )
            ],
        ),
        _fake_order(
            202,
            10,
            "crypto-a",
            12,
            round_order=1400,
            buyer_public_key="pk",
            artifacts=[
                SimpleNamespace(
                    state="active", is_numerai_direct=False, round_tournament=1403
                )
            ],
        ),
        _fake_order(
            203,
            11,
            "static-done",
            8,
            round_order=1400,
            is_per_round=False,
            buyer_public_key="pk",
            artifacts=[
                SimpleNamespace(
                    state="active", is_numerai_direct=False, round_tournament=1400
                )
            ],
        ),
        _fake_order(
            204,
            12,
            "static-missing",
            8,
            round_order=1400,
            is_per_round=False,
            buyer_public_key="pk",
        ),
        _fake_order(
            205,
            13,
            "expired-tournament",
            11,
            round_order=1400,
            buyer_public_key="pk",
        ),
    ]
    monkeypatch.setattr(async_tasks, "datetime", FakeDateTime)
    monkeypatch.setattr(async_tasks.settings, "EMAILS_ENABLED", True)
    monkeypatch.setattr(
        session, "SessionLocal", lambda: SimpleNamespace(close=lambda: None)
    )
    monkeypatch.setattr(
        crud.globals, "get_singleton", lambda db: SimpleNamespace(selling_round=1403)
    )
    monkeypatch.setattr(crud.order, "get_active_orders", lambda db, round_order: orders)
    monkeypatch.setattr(
        numerai,
        "get_numerai_active_round",
        lambda tournament=8: {
            "number": 1403,
            "closeStakingTime": (
                "2026-11-20T12:00:00Z" if tournament == 11 else "2026-11-20T13:05:00Z"
            ),
        },
    )
    monkeypatch.setattr(
        order_deps,
        "send_order_upload_reminder_emails",
        lambda order, close_staking_time=None, round_order=None: reminded.append(
            (order.id, close_staking_time, round_order)
        ),
    )

    async_tasks._run_send_order_artifact_upload_reminder_emails()

    assert reminded == [
        (201, "2026-11-20 13:05 UTC", 1403),
        (204, None, None),
    ]


def test_missed_upload_and_reminder_templates_render(monkeypatch) -> None:
    enqueued = []
    from emails.template import JinjaTemplate

    from app import utils

    monkeypatch.setattr(utils, "_enqueue_email", lambda **kw: enqueued.append(kw))
    utils.send_missed_upload_email(
        "s@ex.com",
        "seller1",
        "101, 102",
        1403,
        "crypto-a",
        "2026-11-20 13:05 UTC",
        is_seller=True,
    )
    utils.send_missed_upload_email("b@ex.com", "buyer1", "108", 1403, "signals-moved")
    utils.send_order_artifact_upload_reminder_email(
        "s@ex.com", "seller1", 201, 1403, "crypto-a", "buyer1", "2026-11-20 13:05 UTC"
    )
    rendered = [
        JinjaTemplate(e["html_template"], environment=utils._HTML_JINJA_ENV).render(
            **e["environment"]
        )
        for e in enqueued
    ]
    assert (
        "101, 102" in rendered[0]
        and "2026-11-20 13:05 UTC" in rendered[0]
        and "delivery was incomplete" in rendered[0]
    )
    assert "108" in rendered[1] and "Staking Closed (UTC)" not in rendered[1]
    assert (
        "Staking Deadline (UTC)" in rendered[2]
        and "2026-11-20 13:05 UTC" in rendered[2]
    )
