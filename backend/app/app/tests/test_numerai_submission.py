from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import pytest
from fastapi import HTTPException

from app.api.dependencies import numerai


def _fake_numerapi(monkeypatch, calls: List[Dict[str, Any]], error=None) -> None:
    class FakeNumerAPI:
        def __init__(self, public_id=None, secret_key=None) -> None:
            pass

        def raw_query(self, query, variables=None, authorization=False):
            calls.append({"query": query, "variables": dict(variables or {})})
            if error is not None:
                raise error
            return {"data": {"create_submission": {"id": "submission-id"}}}

    monkeypatch.setattr(numerai, "NumerAPI", FakeNumerAPI)


def test_validate_numerai_submission_matches_numerapi_create_submission(
    monkeypatch,
) -> None:
    calls: List[Dict[str, Any]] = []
    _fake_numerapi(monkeypatch, calls)

    submission_id = numerai.validate_numerai_submission(
        object_name="predictions.csv", model_id="model-id", tournament=8
    )

    assert submission_id == "submission-id"
    assert len(calls) == 1
    assert "version" not in calls[0]["query"]
    assert calls[0]["variables"] == {
        "filename": "predictions.csv",
        "tournament": 8,
        "modelId": "model-id",
        "triggerId": None,
    }


def test_validate_numerai_submission_fails_without_retry(monkeypatch) -> None:
    calls: List[Dict[str, Any]] = []
    _fake_numerapi(monkeypatch, calls, error=ValueError("Invalid submission"))

    submission_id = numerai.validate_numerai_submission(
        object_name="predictions.csv", model_id="model-id", tournament=8
    )

    assert submission_id is None
    assert len(calls) == 1


def _fake_active_round(
    monkeypatch, calls: List[Dict[str, Any]], number: int, close_staking_time: datetime
) -> None:
    class FakeNumerAPI:
        def __init__(self, public_id=None, secret_key=None) -> None:
            pass

        def raw_query(self, query, variables=None, authorization=False):
            calls.append(dict(variables or {}))
            return {
                "data": {
                    "rounds": [
                        {
                            "number": number,
                            "closeStakingTime": close_staking_time.isoformat(),
                        }
                    ]
                }
            }

    monkeypatch.setattr(numerai, "NumerAPI", FakeNumerAPI)


def test_validate_round_open_uses_product_tournament(monkeypatch) -> None:
    calls: List[Dict[str, Any]] = []
    _fake_active_round(
        monkeypatch, calls, 1397, datetime.now(timezone.utc) + timedelta(minutes=30)
    )

    numerai.validate_round_open(12, 1397)

    assert calls == [{"tournament": 12}]


def test_validate_round_open_rejects_other_round(monkeypatch) -> None:
    _fake_active_round(
        monkeypatch, [], 1396, datetime.now(timezone.utc) + timedelta(minutes=30)
    )

    with pytest.raises(HTTPException):
        numerai.validate_round_open(12, 1397)
