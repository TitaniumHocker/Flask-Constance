import pickle
import typing as t

try:
    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    from sqlalchemy.orm.attributes import flag_modified
except ImportError as err:
    raise ImportError(
        "Flask-SQLAlchemy extension must be installed to use it as a backend for Flask-Constance"
    ) from err

from . import exc
from .core import Backend


class SettingMixin:
    """Model mixin for Flask-SQLAlchemy backend"""

    __abstract__ = True
    __tablename__ = "constance_settings"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256), unique=True, nullable=False, index=True)
    value = sa.Column(sa.PickleType, nullable=True)

    def __repr__(self) -> str:
        return f"<Setting {self.name}>"

    def __str__(self) -> str:
        return t.cast(str, self.name)


class FlaskSQLAlchemyBackend(Backend):
    """Flask-SQLAlchemy backend

    :param model: Model which describes settings.
    :param session: Database session.
    """

    def __init__(self, model: orm.DeclarativeMeta, session: orm.scoped_session):
        self.model = model
        self.session = session

    def get(self, name: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        if instance := self.model.query.filter_by(name=name).first():  # type: ignore
            return instance.value
        raise exc.SettingNotFoundInBackendError(name, self)

    def set(self, name: str, value: t.Any):
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        """
        transaction = self.session.begin(nested=True)
        instance = self.model.query.filter_by(name=name).first()  # type: ignore
        if instance is None:
            instance = self.model(name=name, value=value)
        instance.value = value
        flag_modified(instance, "value")
        transaction.session.add(instance)
        transaction.commit()
