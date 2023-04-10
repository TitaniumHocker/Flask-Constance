import random
import typing as t
from string import ascii_letters

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_constance import Constance
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin
from flask_constance.backends.memory import MemoryBackend
from flask_constance.storage import Storage


def genstr(n: int = 8):
    return "".join(random.choice(ascii_letters) for _ in range(n))


@pytest.fixture(scope="session")
def default_payload():
    return {
        genstr(): genstr(),
        genstr(): [genstr() for _ in range(random.randint(1, 10))],
        genstr(): None,
        genstr(): True,
        genstr(): {genstr(): genstr()},
    }


@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    app.secret_key = genstr()
    yield app


@pytest.fixture
def with_memory_backend(app: Flask, default_payload: t.Dict[str, t.Any]):
    constance = Constance(app)
    app.config["CONSTANCE_PAYLOAD"] = default_payload
    with app.app_context():
        yield constance.storage._backend


@pytest.fixture
def with_fsqla_backend(app: Flask, default_payload: t.Dict[str, t.Any]):
    app.config["CONSTANCE_PAYLOAD"] = default_payload
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    class Setting(db.Model, SettingMixin):
        pass

    backend = FlaskSQLAlchemyBackend(Setting, db.session)
    constance = Constance(app, backend)

    with app.app_context():
        db.create_all()
        yield backend
