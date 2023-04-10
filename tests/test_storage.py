import typing as t

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_constance import Constance, settings
from flask_constance.backends.fsqla import FlaskSQLAlchemyBackend, SettingMixin


@pytest.mark.parametrize("new_value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_set(
    with_memory_backend, default_payload: t.Dict[str, t.Any], new_value: t.Any
):
    for key in default_payload:
        setattr(settings, key, new_value)
        assert getattr(settings, key) == new_value


def test_get(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    for key, value in default_payload.items():
        assert getattr(settings, key) == value


def test_get_undefined(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    with pytest.raises(AttributeError):
        getattr(settings, "awdoiaodjaowdijwaodija")


def test_set_undefined(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    with pytest.raises(AttributeError):
        setattr(settings, "awdoiaodjaowdijwaodija", "aowidjawoidjwaodijoijdwad")


def test_del(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    for name in default_payload:
        setattr(settings, name, "new")
        assert getattr(settings, name) == "new"
        delattr(settings, name)
        assert getattr(settings, name) != "new"


def test_del_undefined(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    with pytest.raises(AttributeError):
        delattr(settings, "unknown-setting")


def test_dir(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    assert sorted(dir(settings)) == sorted(default_payload.keys())


@pytest.fixture
def app_with_db(app: Flask, default_payload: t.Dict[str, t.Any]):
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

    yield app


def test_mut_list(app_with_db: Flask, default_payload: t.Dict[str, t.Any]):
    check_key = None

    with app_with_db.app_context():
        for key, value in default_payload.items():
            if isinstance(value, list):
                value.append(123)
                check_key = key

    assert check_key is not None, "Missing list in generated data."

    with app_with_db.app_context():
        assert getattr(settings, check_key)[-1] == 123


def test_mut_dict(app_with_db: Flask, default_payload: t.Dict[str, t.Any]):
    check_key = None

    with app_with_db.app_context():
        for key, value in default_payload.items():
            if isinstance(value, dict):
                value["qwerty"] = 123
                check_key = key

    assert check_key is not None, "Missing dict in generated data."

    with app_with_db.app_context():
        assert getattr(settings, check_key)["qwerty"] == 123
