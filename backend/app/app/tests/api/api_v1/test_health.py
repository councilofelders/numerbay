from app.core.config import settings


def test_healthz(client) -> None:
    response = client.get(f"{settings.API_V1_STR}/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
