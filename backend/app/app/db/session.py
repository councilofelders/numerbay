from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_timeout=settings.SQLALCHEMY_POOL_TIMEOUT,
    pool_pre_ping=settings.SQLALCHEMY_POOL_PRE_PING,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_with_db_session(func: Callable, *args, **kwargs):
    """Execute a function with a database session and immediately return the result.
    This is a direct call version that doesn't require calling the wrapped function.

    Usage:
        result = run_with_db_session(lambda db: crud.user.get(db, id=1))
    """
    db = SessionLocal()
    try:
        return func(db, *args, **kwargs)
    finally:
        db.close()
