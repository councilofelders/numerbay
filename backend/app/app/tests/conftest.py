from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import async_tasks
from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import authentication_token_from_username
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(autouse=True)
def stub_cloud_tasks_dispatch(monkeypatch):
    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self):
            return {"name": "stub-task"}

    class FakeSession:
        def post(self, url, json):
            return FakeResponse()

    monkeypatch.setattr(async_tasks, "_get_cloud_tasks_session", lambda: FakeSession())
    monkeypatch.setattr(
        async_tasks.settings,
        "ASYNC_WORKER_DISPATCH_URL",
        "https://worker.example.com/backend-api/v1/internal/tasks/dispatch",
    )
    monkeypatch.setattr(async_tasks.settings, "ASYNC_WORKER_DISPATCH_TOKEN", "test")


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_username(
        client=client, username=settings.EMAIL_TEST_USER, db=db
    )
