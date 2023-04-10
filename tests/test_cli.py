import json
import typing as t

import pytest
from flask import Flask
from flask.testing import FlaskCliRunner

from flask_constance import Constance, settings


@pytest.fixture
def clirunner(app: Flask, default_payload: t.Dict[str, t.Any]):
    constance = Constance(app)
    app.config["CONSTANCE_PAYLOAD"] = default_payload
    with app.app_context():
        yield app.test_cli_runner()


def test_get_all(clirunner: FlaskCliRunner):
    result = clirunner.invoke(args=["constance", "get"])
    for name in dir(settings):
        assert name in result.output
    assert result.exit_code == 0


def test_get_one(clirunner: FlaskCliRunner):
    for name in dir(settings):
        result = clirunner.invoke(args=["constance", "get", name])
        assert name in result.output
        assert result.exit_code == 0


def test_get_unknown(clirunner: FlaskCliRunner):
    result = clirunner.invoke(args=["constance", "get", "something_unknown_thing"])
    assert result.exit_code > 0


def test_set(clirunner: FlaskCliRunner):
    for name in dir(settings):
        result = clirunner.invoke(
            args=["constance", "set", name, json.dumps("something_new")]
        )
        assert result.exit_code == 0
        assert (
            "something_new" in clirunner.invoke(args=["constance", "get", name]).output
        )


def test_set_unknown(clirunner: FlaskCliRunner):
    result = clirunner.invoke(
        args=["constance", "set", "something-unknown", json.dumps("data")]
    )
    assert result.exit_code > 0
    assert "Unknown" in result.output


def test_set_invalid_json(clirunner: FlaskCliRunner):
    for name in dir(settings):
        result = clirunner.invoke(args=["constance", "set", name, "invalid-json"])
        assert result.exit_code > 0
        assert "Failed to update" in result.output


def test_delete(clirunner: FlaskCliRunner):
    for name in dir(settings):
        result = clirunner.invoke(args=["constance", "del", name])
        assert result.exit_code == 0
        assert "successfully deleted" in result.output


def test_delete_unknown(clirunner: FlaskCliRunner):
    result = clirunner.invoke(args=["constance", "del", "unknown-name"])
    assert result.exit_code > 0
    assert "Unknown" in result.output
