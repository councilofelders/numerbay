"""One-time backfill: encrypt user Numerai API secrets (idempotent).

Run against the prod database with DATA_ENCRYPTION_KEY set, e.g. via
cloud-sql-proxy with the app role:

    DATA_ENCRYPTION_KEY=... POSTGRES_SERVER=127.0.0.1 ... \
        python -m app.backfill_encrypt_keys
"""

from app.core import crypto
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User


def backfill() -> None:
    """Encrypt all plaintext secrets in the original column, in place"""
    if not settings.DATA_ENCRYPTION_KEY:
        raise RuntimeError("DATA_ENCRYPTION_KEY is not set")

    db = SessionLocal()
    try:
        users = (
            db.query(User)
            .filter(
                User.numerai_api_key_secret_stored.isnot(None),
                ~User.numerai_api_key_secret_stored.startswith("gAAA"),
            )
            .with_for_update()
            .all()
        )
        print(f"rows to encrypt: {len(users)}")
        for user in users:
            user.numerai_api_key_secret_stored = crypto.encrypt_secret(
                user.numerai_api_key_secret_stored  # type: ignore[arg-type]
            )
        db.commit()

        rows = (
            db.query(User).filter(User.numerai_api_key_secret_backup.isnot(None)).all()
        )
        unencrypted = [
            user.id
            for user in rows
            if user.numerai_api_key_secret_stored is None
            or not user.numerai_api_key_secret_stored.startswith("gAAA")
        ]
        mismatched = [
            user.id
            for user in rows
            if user.numerai_api_key_secret_stored is not None
            and user.numerai_api_key_secret_stored.startswith("gAAA")
            and crypto.decrypt_secret(user.numerai_api_key_secret_stored)
            != user.numerai_api_key_secret_backup
        ]
        print(
            f"verified {len(rows)} rows, "
            f"unencrypted: {len(unencrypted)}, mismatches: {len(mismatched)}"
        )
        if unencrypted or mismatched:
            raise RuntimeError(
                f"backfill verification failed: "
                f"unencrypted={unencrypted}, mismatched={mismatched}"
            )
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
