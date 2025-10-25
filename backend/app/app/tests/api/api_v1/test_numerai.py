from unittest.mock import Mock, patch

import requests
from fastapi.testclient import TestClient

from app.core.config import settings


def test_numerai_graphql_proxy_success(client: TestClient) -> None:
    """Test successful GraphQL proxy request"""
    # Mock response data
    mock_response_data = {
        "data": {
            "v2RoundModelPerformances": [
                {
                    "roundNumber": 456,
                    "atRisk": "10.5",
                    "submissionScores": [
                        {
                            "displayName": "corr",
                            "value": 0.0123,
                            "percentile": 0.6789,
                        }
                    ],
                }
            ]
        }
    }

    # Test payload
    test_payload = {
        "query": "query v2RoundModelPerformances($model_id: String!, $lastNRounds: Integer!, $tournament: Integer!) { v2RoundModelPerformances(distinctOnRound: true, modelId: $model_id, lastNRounds: $lastNRounds, tournament: $tournament) { roundNumber atRisk } }",
        "variables": {"model_id": "test_model", "lastNRounds": 5, "tournament": 8},
    }

    # Mock requests.post to simulate successful Numerai API response
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = client.post(
            f"{settings.API_V1_STR}/numerai/graphql-proxy", json=test_payload
        )

        assert response.status_code == 200
        assert response.json() == mock_response_data

        # Verify the proxy called the correct endpoint
        mock_post.assert_called_once_with(
            "https://api-tournament.numer.ai/",
            json=test_payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30,
        )


def test_numerai_graphql_proxy_api_error(client: TestClient) -> None:
    """Test GraphQL proxy with Numerai API error"""
    test_payload = {
        "query": "invalid query",
        "variables": {},
    }

    # Mock requests.post to simulate Numerai API error
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("API Error")

        response = client.post(
            f"{settings.API_V1_STR}/numerai/graphql-proxy", json=test_payload
        )

        assert response.status_code == 502
        assert "Failed to proxy request to Numerai API" in response.json()["detail"]


def test_numerai_graphql_proxy_timeout(client: TestClient) -> None:
    """Test GraphQL proxy with timeout error"""
    test_payload = {
        "query": "query { __typename }",
        "variables": {},
    }

    # Mock requests.post to simulate timeout
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout("Request timeout")

        response = client.post(
            f"{settings.API_V1_STR}/numerai/graphql-proxy", json=test_payload
        )

        assert response.status_code == 502
        assert "Failed to proxy request to Numerai API" in response.json()["detail"]
        assert "Request timeout" in response.json()["detail"]


def test_numerai_graphql_proxy_http_error(client: TestClient) -> None:
    """Test GraphQL proxy with HTTP error from Numerai API"""
    test_payload = {
        "query": "query { __typename }",
        "variables": {},
    }

    # Mock requests.post to simulate HTTP error
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "400 Bad Request"
        )
        mock_post.return_value = mock_response

        response = client.post(
            f"{settings.API_V1_STR}/numerai/graphql-proxy", json=test_payload
        )

        assert response.status_code == 502
        assert "Failed to proxy request to Numerai API" in response.json()["detail"]
