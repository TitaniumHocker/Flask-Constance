import typing as t

import pytest
from flask import Flask, current_app
from flask.testing import FlaskClient

from flask_constance import Constance, settings


@pytest.fixture
def testclient(app: Flask, default_payload: t.Dict[str, t.Any]):
    constance = Constance(app, view_base_url="/api/constance")
    app.config["CONSTANCE_PAYLOAD"] = default_payload
    with app.app_context():
        yield app.test_client()


def test_get_all(testclient: FlaskClient):
    response = testclient.get("/api/constance")
    assert response.status == "200 OK"
    for name in dir(settings):
        assert name in response.json


def test_get_one(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.get(f"/api/constance/{name}")
        assert response.status == "200 OK"
        assert name in response.json


def test_get_unknown(testclient: FlaskClient):
    response = testclient.get("/api/constance/something-unknown")
    assert response.status == "404 NOT FOUND"


def test_set(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.put(f"/api/constance/{name}", json="new")
        assert response.status == "200 OK"
        get_response = testclient.get(f"/api/constance/{name}")
        assert get_response.status == "200 OK"
        assert get_response.json[name] == "new"


def test_set_unknown(testclient: FlaskClient):
    response = testclient.put("/api/constance/something-unknown", json="new")
    assert response.status == "404 NOT FOUND"


def test_set_invalid(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.put(f"/api/constance/{name}", data="invalid-json")
        assert response.status == "400 BAD REQUEST"


def test_delete(testclient: FlaskClient):
    for name in dir(settings):
        response = testclient.put(f"/api/constance/{name}", json="some-new-data")
        assert response.status == "200 OK"
    for name in dir(settings):
        response = testclient.get(f"/api/constance/{name}")
        assert response.status == "200 OK"
        assert response.json != current_app.config["CONSTANCE_PAYLOAD"][name]
    for name in dir(settings):
        response = testclient.delete(f"/api/constance/{name}")
        assert response.status == "200 OK"
        get_response = testclient.get(f"/api/constance/{name}")
        assert get_response.status == "200 OK"
        assert get_response.json[name] == current_app.config["CONSTANCE_PAYLOAD"][name]


def test_delete_unknown(testclient: FlaskClient):
    response = testclient.delete("/api/constance/something-unknown")
    assert response.status == "404 NOT FOUND"
