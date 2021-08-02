import pickle
import typing as t

import sqlalchemy as sa

from .core import Backend


class SettingMixin:
    """Model mixin for Flask-SQLAlchemy backend"""

    __tablename__ = "constance_settings"
    id = sa.Column(sa.Integer, primary_key=True)
    key = sa.Column(sa.String(256), unique=True, nullable=False, index=True)
    value = sa.Column(sa.PickleType, nullable=True)

    def __repr__(self) -> str:
        return f"<Setting {self.key}>"

    def __str__(self) -> str:
        return self.key


class FlaskSQLAlchemyBackend(Backend):
    """Flask-SQLAlchemy backend

    :param model: Model which describes settings.
    :param session: Database session.
    """

    def __init__(self, model: sa.orm.DeclarativeMeta, session: sa.orm.Session):
        self.model = model
        self.session = session

    def get(self, key: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        setting = self.model.query.filter_by(key=key).first()
        if setting is None:
            return None
        return pickle.loads(setting.value)

    def set(self, key: str, value: t.Any) -> t.Any:
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        :returns: Old value of the setting.
        """
        setting = self.model.query.filter_by(key=key).first()
        if setting is None:
            old = None
            setting = self.model(key=key, value=pickle.dumps(value))
        else:
            old = pickle.loads(setting.value)
            setting.value = pickle.dumps(value)

        self.session.add(setting)
        self.session.commit()

        return old
