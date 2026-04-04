from app.core.config import settings


def test_internal_dispatch_requires_token(client) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/internal/tasks/dispatch",
        json={"task": "send-email", "args": [], "kwargs": {}},
    )

    assert response.status_code == 503


def test_internal_dispatch_runs_allowlisted_task(client, monkeypatch) -> None:
    called = []
    token = "dispatch-secret"

    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(internal.settings, "ASYNC_WORKER_DISPATCH_TOKEN", token)
    monkeypatch.setattr(
        internal,
        "run_async_task",
        lambda task, args=None, kwargs=None: called.append((task, args, kwargs)),
    )

    response = client.post(
        f"{settings.API_V1_STR}/internal/tasks/dispatch",
        headers={"X-Internal-Task-Token": token},
        json={"task": "send-email", "args": [], "kwargs": {"email_to": "x@y.z"}},
    )

    assert response.status_code == 200
    assert called == [("send-email", [], {"email_to": "x@y.z"})]


def test_internal_payment_reconcile_requires_token(client, monkeypatch) -> None:
    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(
        internal.settings,
        "ASYNC_WORKER_DISPATCH_TOKEN",
        "dispatch-secret",
    )

    response = client.post(f"{settings.API_V1_STR}/internal/reconcile/payments")

    assert response.status_code == 403


def test_internal_payment_reconcile_queues_pending_orders(client, monkeypatch) -> None:
    token = "dispatch-secret"

    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(internal.settings, "ASYNC_WORKER_DISPATCH_TOKEN", token)
    monkeypatch.setattr(internal, "enqueue_pending_payment_updates", lambda: 3)

    response = client.post(
        f"{settings.API_V1_STR}/internal/reconcile/payments",
        headers={"X-Internal-Task-Token": token},
    )

    assert response.status_code == 200
    assert response.json() == {"queued": 3}
