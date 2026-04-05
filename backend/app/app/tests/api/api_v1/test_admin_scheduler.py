import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.api.api_v1.endpoints import admin, scheduler
from app.core.config import settings
from app.tests.utils.order import get_random_order


@pytest.mark.parametrize(
    "route,job_name",
    [
        ("stake", "validate-numerai-models-stake"),
        ("stake-snapshot", "stake-snapshots"),
        ("update-polls", "polls"),
        ("prune-storage", "prune-storage"),
        ("artifact-reminder", "artifact-reminders"),
        ("product-stats", "product-sales-stats"),
    ],
)
def test_scheduler_manual_routes_run_direct_jobs(
    client: TestClient,
    superuser_token_headers: dict,
    monkeypatch,
    route: str,
    job_name: str,
) -> None:
    calls = []

    monkeypatch.setattr(scheduler, "run_job", lambda name: calls.append(name))

    response = client.post(
        f"{settings.API_V1_STR}/scheduler/{route}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success!"}
    assert calls == [job_name]


def test_scheduler_numerai_models_route_enqueues_batch_update(
    client: TestClient,
    superuser_token_headers: dict,
    monkeypatch,
) -> None:
    calls = []

    monkeypatch.setattr(
        scheduler,
        "enqueue_batch_update_numerai_models",
        lambda: calls.append("models") or {"name": "task-created"},
    )

    response = client.post(
        f"{settings.API_V1_STR}/scheduler/numerai-models",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success!"}
    assert calls == ["models"]


def test_scheduler_numerai_model_scores_route_enqueues_batch_update(
    client: TestClient,
    superuser_token_headers: dict,
    monkeypatch,
) -> None:
    calls = []

    monkeypatch.setattr(
        scheduler,
        "enqueue_batch_update_numerai_model_scores",
        lambda: calls.append("scores") or {"name": "task-created"},
    )

    response = client.post(
        f"{settings.API_V1_STR}/scheduler/numerai-model-scores",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success!"}
    assert calls == ["scores"]


def test_scheduler_submit_route_enqueues_batch_submission_seed(
    client: TestClient,
    superuser_token_headers: dict,
    monkeypatch,
) -> None:
    calls = []

    monkeypatch.setattr(
        scheduler,
        "enqueue_batch_submit_numerai_models",
        lambda: calls.append("submit") or {"name": "task-created"},
    )

    response = client.post(
        f"{settings.API_V1_STR}/scheduler/submit",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "success!"}
    assert calls == ["submit"]


@pytest.mark.parametrize(
    "path",
    [
        "/scheduler/get_schedules",
        "/scheduler/test",
        "/scheduler/round-rollover",
        "/utils/test-celery/",
    ],
)
def test_removed_manual_celery_routes_are_not_found(
    client: TestClient,
    superuser_token_headers: dict,
    path: str,
) -> None:
    request = client.get if path.endswith("get_schedules") else client.post
    response = request(f"{settings.API_V1_STR}{path}", headers=superuser_token_headers)

    assert response.status_code == 404


def test_admin_resubmit_for_order_runs_submission_check_directly(
    client: TestClient,
    superuser_token_headers: dict,
    monkeypatch,
    db: Session,
) -> None:
    current_user = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers,
    ).json()
    calls = []

    monkeypatch.setattr(
        admin,
        "enqueue_check_numerai_submission",
        lambda order_json, retry=True, delay_seconds=None: calls.append(
            (order_json, retry, delay_seconds)
        ),
    )

    with get_random_order(db, buyer_id=current_user["id"]) as order:
        order_id = order.id
        crud.order.update(
            db,
            db_obj=order,
            obj_in={"state": "confirmed", "submit_model_id": "model-1"},
        )

        response = client.post(
            f"{settings.API_V1_STR}/admin/resubmit-for-order",
            params={"order_id": order_id},
            headers=superuser_token_headers,
        )

    assert response.status_code == 200
    assert response.json() == {"msg": "success!"}
    assert len(calls) == 1
    assert calls[0][0]["id"] == order_id
    assert calls[0][1] is False
    assert calls[0][2] is None
