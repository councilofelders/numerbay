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


def test_internal_active_round_reconcile_queues_sync(client, monkeypatch) -> None:
    token = "dispatch-secret"
    calls = []

    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(internal.settings, "ASYNC_WORKER_DISPATCH_TOKEN", token)
    monkeypatch.setattr(
        internal,
        "get_current_scheduler_slot",
        lambda now=None: now.strftime("%Y%m%d%H%M") if now else "fallback-slot",
    )
    monkeypatch.setattr(
        internal,
        "enqueue_update_active_round",
        lambda schedule_slot=None: calls.append(schedule_slot),
    )

    response = client.post(
        f"{settings.API_V1_STR}/internal/reconcile/active-round",
        headers={
            "X-Internal-Task-Token": token,
            "X-CloudScheduler-ScheduleTime": "2026-04-05T09:00:17Z",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success"}
    assert calls == ["202604050900"]


def test_internal_model_scores_reconcile_queues_sync(client, monkeypatch) -> None:
    token = "dispatch-secret"
    calls = []

    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(internal.settings, "ASYNC_WORKER_DISPATCH_TOKEN", token)
    monkeypatch.setattr(
        internal,
        "get_current_scheduler_slot",
        lambda now=None: now.strftime("%Y%m%d%H%M") if now else "fallback-slot",
    )
    monkeypatch.setattr(
        internal,
        "get_batch_update_numerai_model_scores_dedupe_key",
        lambda slot: f"model-scores-{slot}",
    )
    monkeypatch.setattr(
        internal,
        "enqueue_batch_update_numerai_model_scores",
        lambda retries=0, delay_seconds=None, dedupe_key=None: calls.append(
            (retries, delay_seconds, dedupe_key)
        ),
    )

    response = client.post(
        f"{settings.API_V1_STR}/internal/reconcile/numerai-model-scores",
        headers={
            "X-Internal-Task-Token": token,
            "X-CloudScheduler-ScheduleTime": "2026-04-05T14:05:59Z",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success"}
    assert calls == [(10, None, "model-scores-202604051405")]


def test_internal_model_scores_reconcile_invalid_scheduler_time(client, monkeypatch) -> None:
    token = "dispatch-secret"

    from app.api.api_v1.endpoints import internal

    monkeypatch.setattr(internal.settings, "ASYNC_WORKER_DISPATCH_TOKEN", token)

    response = client.post(
        f"{settings.API_V1_STR}/internal/reconcile/numerai-model-scores",
        headers={
            "X-Internal-Task-Token": token,
            "X-CloudScheduler-ScheduleTime": "not-a-time",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid Cloud Scheduler schedule time"}
