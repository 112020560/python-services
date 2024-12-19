import typing
from contextlib import contextmanager

from sentry_sdk import capture_exception
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from src.constants import DB_ECHO, DB_PRE_PING

Session = scoped_session(sessionmaker(expire_on_commit=False))
_session = None


def bind_engine(**kwargs):
    engine = create_engine(
        kwargs.get("url") or URL(**kwargs),
        echo=DB_ECHO,
        pool_pre_ping=DB_PRE_PING,
    )
    Session.configure(bind=engine)
    return Session


def get_session(**settings):
    global _session

    if _session:
        return _session

    _session = bind_engine(**settings)
    return _session


def clear_session():
    global _session

    if _session:
        _session.connection().detach()
        _session.close()
        _session = None


@contextmanager
def session_scope():
    try:
        yield Session
        Session.commit()
    except Exception:
        Session.rollback()
        capture_exception()
        raise
    finally:
        Session.close()


@contextmanager
def commit_or_rollback_context() -> typing.Iterator[scoped_session]:
    try:
        yield Session
        Session.commit()
    except Exception:
        Session.rollback()
        raise
