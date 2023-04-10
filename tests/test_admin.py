import typing as t

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_admin import Admin

from flask_constance import Constance, settings
from flask_constance.admin import ConstanceAdminView


@pytest.fixture
def testclient(app: Flask, default_payload: t.Dict[str, t.Any]):
    constance = Constance(app, view_base_url="/api/constance")
    app.config["CONSTANCE_PAYLOAD"] = default_payload
    app.config["WTF_CSRF_ENABLED"] = False
    admin = Admin(app, template_mode="bootstrap4")
    admin.add_view(ConstanceAdminView(name="Settings", endpoint="settings"))
    with app.app_context():
        yield app.test_client()


def test_index(testclient: FlaskClient):
    response = testclient.get("/admin/settings/")
    assert response.status == "200 OK"
    for name in dir(settings):
        assert f"<b>{name}</b>" in response.data.decode()


def test_update(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.post(
            "/admin/settings/",
            data={
                "name": name,
                "value": '"new-value"',
                "submit": "save",
            },
        )
        assert response.status == "302 FOUND"
        assert getattr(settings, name) == "new-value"


def test_invalid(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.post(
            "/admin/settings/",
            data={
                "name": name,
                "value": "invalid-shit",
                "submit": "save",
            },
        )
        assert response.status == "302 FOUND"
        assert getattr(settings, name) != "invalid-shit"
        redirected = testclient.get(response.headers["Location"])
        assert redirected.status == "200 OK"
        assert "update failed" in redirected.data.decode()


def test_reset(testclient: FlaskClient):
    for name in dir(settings):
        setattr(settings, name, "new-value")
        assert getattr(settings, name) == "new-value"
        response = testclient.post(
            "/admin/settings/",
            data={
                "name": name,
                "value": '"something"',
                "reset": "reset",
            },
        )
        assert response.status == "302 FOUND"
        assert getattr(settings, name) != "new-value"
