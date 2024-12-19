import warnings
from base64 import b64decode, b64encode

from sqlalchemy import Column, DateTime, MetaData, Numeric, cast, func, select, types
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm.exc import NoResultFound

from src.utils import session
from src.utils.datetime import utc_now

# Avoid circular dependencies
Session = session.Session  # type: ignore
commit_or_rollback_context = session.commit_or_rollback_context  # type: ignore

ENCODING = "utf-8"
SEPARATOR = "-"
SCHEMA = "public"


class Base:
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    update_allowed_keys: tuple[str, ...] = ()

    @classmethod
    def get(cls, id=None, **kwargs):  # noqa: A002
        query_result = cls.get_or_none(id, **kwargs)

        if not query_result:
            raise NoResultFound(
                "No row was found for get()",
                cls.__name__,
                str({**({"id": id} if id is not None else {}), **kwargs}),
            )

        return query_result

    @classmethod
    def get_with_lock(cls, id=None, **kwargs):  # noqa: A002
        if id:
            return Session.query(cls).with_for_update().get(id)

        return Session.query(cls).filter_by(**kwargs).with_for_update().one()

    @classmethod
    def get_or_none(cls, id=None, **kwargs):  # noqa: A002
        if not id and not kwargs:
            return None

        if id and int(id):
            kwargs = {"id": id}

        return cls.filter_by(**kwargs).first()

    @classmethod
    def get_all(cls, *args, **kwargs):
        query = cls.query()

        # Convert list kwargs to args
        list_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, list)}
        for k, v in list_kwargs.items():
            args += (getattr(cls, k).in_(v),)
            kwargs.pop(k)

        if args:
            query = query.filter(*args)
        if kwargs:
            query = query.filter_by(**kwargs)

        return query.all()

    @classmethod
    def exists(cls, **kwargs):
        return Session.query(
            cls.filter_by(**kwargs).exists(),
        ).scalar()

    @classmethod
    def filter(cls, *args):
        return cls.query().filter(*args)

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query().filter_by(**kwargs)

    @classmethod
    def join(cls, *args):
        return cls.query().join(*args)

    @classmethod
    def query(cls):
        return Session.query(cls)

    @classmethod
    def count(cls, **kwargs):
        return cls.execute(
            cls.filter_by(**kwargs)
            .statement.with_only_columns(
                [func.count()],
            )
            .order_by(None),
        ).scalar()

    @classmethod
    def execute(cls, statement):
        return Session.execute(statement)

    @classmethod
    def create(cls, **kwargs):
        with commit_or_rollback_context():
            instance = cls(**kwargs)
            Session.add(instance)

            return instance

    @classmethod
    def get_by(cls, **kwargs):
        warnings.warn("Deprecated: use get()", DeprecationWarning)
        return cls.get(**kwargs)

    @classmethod
    def one_or_none(cls, **kwargs):
        warnings.warn("Deprecated: use get_or_none()", DeprecationWarning)
        return cls.get_or_none(**kwargs)

    @classmethod
    def get_by_name(cls, name):
        warnings.warn("Deprecated: use get(name=)", DeprecationWarning)
        return cls.get(name=name)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def update(self, **kwargs):
        with commit_or_rollback_context():
            for key, value in kwargs.items():
                if self.update_allowed_keys and key not in self.update_allowed_keys:
                    raise Exception(f"Can't update key: {key}")
                setattr(self, key, value)
            return self

    def reload(self):
        Session.refresh(self)

        return self

    def commit(self):
        with commit_or_rollback_context():
            return self


Model = declarative_base(cls=Base, metadata=MetaData(schema=SCHEMA))


def encode_id(id: str | int, klass: str) -> str:  # noqa: A002
    global_id = f"{klass}{SEPARATOR}{id}"
    encoded_id = b64encode(bytes(global_id, ENCODING))
    return encoded_id.decode(ENCODING)


def decode_id(id: str) -> list[str]:  # noqa: A002
    decoded_id = b64decode(id).decode(ENCODING)
    return decoded_id.split(SEPARATOR)


class CastToNumericType(types.TypeDecorator):
    """Converts stored Money values to Numeric via CAST operation."""

    impl = types.Numeric

    def column_expression(self, col):
        return cast(col, Numeric)


class BaseDeclarativeMeta(DeclarativeMeta, type):
    def __getattr__(cls, name):
        # SQL Alchemy methods
        if name.startswith("_sa") or "_cls__" in name:
            raise AttributeError

        # Compatibility with ModelStatuses.STATUS_NAME
        if name.startswith("STATUS_"):
            _, status = name.split("STATUS_")
            return cls.get_value(status)

        # Define get_status methods
        if name.startswith("get_"):
            _, status = name.split("get_")

            def getter():
                return cls.get(name=cls.get_value(status))

            return getter

        # Model.statuses.NAME
        return cls.get_value(name)

    def get_value(cls, name):
        name = name.upper()

        if name not in cls.all():
            raise AttributeError(name)
        return name


class StatusesMeta(BaseDeclarativeMeta, type):
    """Generates magic methods for Statuses classes."""

    def all(cls):
        return cls.statuses


class TypesMeta(BaseDeclarativeMeta, type):
    """Generates magic methods for Type classes."""

    def all(cls):
        return cls.types


class LevelsMeta(BaseDeclarativeMeta, type):
    """Generates magic methods for Type classes."""

    def all(cls):
        return cls.levels


class StatusModel(Model, metaclass=StatusesMeta):
    __abstract__ = True

    @classmethod
    def select_id_for_status(cls, status):
        return select([cls.id]).where(
            cls.name == status,
        )
