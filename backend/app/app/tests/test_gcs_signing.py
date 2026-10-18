"""Tests for GCS signed URL generation.

Covers the credential-dispatch logic in
``app.api.dependencies.order_artifacts._get_gcs_signing_kwargs``: local
signing for service-account JSON credentials, IAM signing for Cloud Run
metadata credentials, and rejection of unusable or unsupported credentials.
All external calls (ADC, refresh, blob signing) are mocked.
"""

from unittest import mock

import pytest
from google.auth.compute_engine import credentials as compute_credentials
from google.auth.credentials import Signing

from app.api.dependencies import order_artifacts


class FakeSigningCredentials(Signing):
    """Stand-in for service-account JSON credentials (locally signing)."""

    def __init__(self, signer_email="json-sa@numerbay.iam.gserviceaccount.com"):
        self._signer_email = signer_email

    @property
    def signer_email(self):
        return self._signer_email

    @property
    def signer(self):
        return self

    def sign_bytes(self, message):
        return b"fake-signature"


def test_signing_kwargs_json_credentials(monkeypatch) -> None:
    creds = FakeSigningCredentials()
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )

    kwargs = order_artifacts._get_gcs_signing_kwargs()
    assert kwargs == {"credentials": creds}


def test_signing_kwargs_cloud_run(monkeypatch) -> None:
    creds = mock.MagicMock(spec=compute_credentials.Credentials)
    creds.service_account_email = "numerbay-runtime@numerbay.iam.gserviceaccount.com"
    creds.token = "fake-access-token"
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )
    monkeypatch.setattr(
        order_artifacts.google.auth.transport.requests, "Request", mock.MagicMock
    )
    creds.refresh = mock.MagicMock()

    kwargs = order_artifacts._get_gcs_signing_kwargs()
    creds.refresh.assert_called_once()
    assert kwargs == {
        "credentials": creds,
        "service_account_email": "numerbay-runtime@numerbay.iam.gserviceaccount.com",
        "access_token": "fake-access-token",
    }


def test_signing_kwargs_cloud_run_missing_email(monkeypatch) -> None:
    creds = mock.MagicMock(spec=compute_credentials.Credentials)
    creds.service_account_email = None
    creds.token = "fake-access-token"
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )
    monkeypatch.setattr(
        order_artifacts.google.auth.transport.requests, "Request", mock.MagicMock
    )

    with pytest.raises(RuntimeError, match="service account"):
        order_artifacts._get_gcs_signing_kwargs()


def test_signing_kwargs_cloud_run_default_email(monkeypatch) -> None:
    creds = mock.MagicMock(spec=compute_credentials.Credentials)
    creds.service_account_email = "default"
    creds.token = "fake-access-token"
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )
    monkeypatch.setattr(
        order_artifacts.google.auth.transport.requests, "Request", mock.MagicMock
    )

    with pytest.raises(RuntimeError, match="service account"):
        order_artifacts._get_gcs_signing_kwargs()


def test_signing_kwargs_cloud_run_missing_token(monkeypatch) -> None:
    creds = mock.MagicMock(spec=compute_credentials.Credentials)
    creds.service_account_email = "numerbay-runtime@numerbay.iam.gserviceaccount.com"
    creds.token = None
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )
    monkeypatch.setattr(
        order_artifacts.google.auth.transport.requests, "Request", mock.MagicMock
    )

    with pytest.raises(RuntimeError, match="service account"):
        order_artifacts._get_gcs_signing_kwargs()


def test_signing_kwargs_unsupported_credentials(monkeypatch) -> None:
    creds = mock.MagicMock()  # neither Signing nor compute_engine
    monkeypatch.setattr(
        order_artifacts.google.auth,
        "default",
        lambda scopes=None: (creds, "numerbay"),
    )

    with pytest.raises(RuntimeError, match="Unsupported credentials"):
        order_artifacts._get_gcs_signing_kwargs()


def test_generate_gcs_signed_url_uses_kwargs(monkeypatch) -> None:
    kwargs = {
        "credentials": mock.MagicMock(),
        "service_account_email": "numerbay-runtime@numerbay.iam.gserviceaccount.com",
        "access_token": "fake-access-token",
    }
    monkeypatch.setattr(
        order_artifacts, "_get_gcs_signing_kwargs", lambda: dict(kwargs)
    )

    bucket = mock.MagicMock()
    blob = mock.MagicMock()
    blob.generate_signed_url.return_value = "https://signed.example.com"
    bucket.blob.return_value = blob

    url = order_artifacts.generate_gcs_signed_url(
        bucket, "test-object.csv", action="PUT"
    )

    assert url == "https://signed.example.com"
    bucket.blob.assert_called_once_with("test-object.csv")
    _, called_kwargs = blob.generate_signed_url.call_args
    assert called_kwargs["method"] == "PUT"
    assert called_kwargs["version"] == "v4"
    assert called_kwargs["service_account_email"] == kwargs["service_account_email"]
    assert called_kwargs["access_token"] == kwargs["access_token"]
