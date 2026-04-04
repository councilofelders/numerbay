import base64
import json

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
    assert (
        http_request["headers"]["X-Internal-Task-Token"] == "secret"
    )
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


def test_run_update_payment_reschedules_pending_orders(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(async_tasks.settings, "ASYNC_OWNER_PAYMENTS", "gcp")
    monkeypatch.setattr(
        async_tasks.settings, "ORDER_PAYMENT_POLL_FREQUENCY_SECONDS", 20.0
    )
    monkeypatch.setattr(async_tasks, "_run_update_payment_in_db", lambda order_id: None)
    monkeypatch.setattr(async_tasks, "_get_order_state", lambda order_id: "pending")
    monkeypatch.setattr(
        async_tasks,
        "enqueue_update_payment",
        lambda order_id, delay_seconds=None: calls.append((order_id, delay_seconds)),
    )

    async_tasks.run_async_task(async_tasks.TASK_UPDATE_PAYMENT, args=[42])

    assert calls == [(42, 20.0)]
