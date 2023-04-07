import typing as t

try:
    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    from sqlalchemy.orm.attributes import flag_modified
except ImportError as err:
    raise ImportError(
        "Flask-SQLAlchemy extension must be installed to use it as a backend for Flask-Constance"
    ) from err

from .base import Backend


class SettingMixin:
    """Model mixin for Flask-SQLAlchemy backend"""

    __abstract__ = True
    __tablename__ = "constance_settings"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256), unique=True, nullable=False, index=True)
    value = sa.Column(sa.JSON, nullable=True)

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
        instance = self.model.query.filter_by(name=name).first()  # type: ignore
        if instance is not None:
            return instance.value
        raise KeyError(name)

    def set(self, name: str, value: t.Any) -> None:
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
