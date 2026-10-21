""" Symmetric encryption for stored credentials """

from cryptography.fernet import Fernet

from app.core.config import settings


def encrypt_secret(plaintext: str) -> str:
    """Encrypt a secret with the configured Fernet key"""
    if not settings.DATA_ENCRYPTION_KEY:
        raise RuntimeError("DATA_ENCRYPTION_KEY is not set")
    return (
        Fernet(settings.DATA_ENCRYPTION_KEY.encode())
        .encrypt(plaintext.encode())
        .decode()
    )


def decrypt_secret(token: str) -> str:
    """Decrypt a Fernet token with the configured key

    :raises cryptography.fernet.InvalidToken: if the key is wrong or data tampered
    """
    if not settings.DATA_ENCRYPTION_KEY:
        raise RuntimeError("DATA_ENCRYPTION_KEY is not set")
    return (
        Fernet(settings.DATA_ENCRYPTION_KEY.encode()).decrypt(token.encode()).decode()
    )
