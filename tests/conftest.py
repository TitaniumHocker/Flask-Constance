import random
from string import ascii_letters

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_constance import Constance
from flask_constance.backends.core import Backend
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin
from flask_constance.backends.memory import MemoryBackend
from flask_constance.backends.redis import RedisBackend


def genstr(n: int = 8):
    return "".join(random.choice(ascii_letters) for _ in range(n))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    Constance(app)
    with app.app_context():
        yield app


@pytest.fixture
def dummy_backend():
    class DummyBackend(Backend):
        pass

    backend = DummyBackend()
    return backend


@pytest.fixture
def memory_backend():
    backend = MemoryBackend()
    return backend


@pytest.fixture
def fsqla_backend():
    app = Flask(__name__)
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    class Setting(db.Model, SettingMixin):
        pass

    backend = FlaskSQLAlchemyBackend(Setting, db.session)

    with app.app_context():
        db.create_all()
        yield backend


@pytest.fixture
def redis_backend(redisdb):
    app = Flask(__name__)
    app.testing = True

    backend = RedisBackend(redisdb)

    with app.app_context():
        yield backend
