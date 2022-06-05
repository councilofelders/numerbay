import random
import string
from decimal import Decimal
from typing import Dict, Optional

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string(prefix: Optional[str] = None) -> str:
    generated_string = "".join(random.choices(string.ascii_lowercase, k=32))
    if prefix is not None:
        return prefix + generated_string
    return generated_string


def random_decimal() -> Decimal:
    return Decimal(random.random()).quantize(Decimal(10) ** -2)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
