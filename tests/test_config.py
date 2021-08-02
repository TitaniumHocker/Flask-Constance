from string import ascii_letters

import pytest

from conftest import genstr
from flask_constance import config
from flask_constance.const import CONSTANCE_SETTINGS


@pytest.mark.parametrize(
    "key",
    (
        genstr(),
        genstr(),
        genstr(),
    ),
)
@pytest.mark.parametrize(
    "value", (123, False, "shit", {"a": "b"}, ascii_letters.split())
)
def test_getting_setting(app, key, value):
    app.config[CONSTANCE_SETTINGS][key] = 1
    setattr(config, key, value)
    assert getattr(config, key) == value


@pytest.mark.parametrize(
    "key",
    (
        genstr(),
        genstr(),
        genstr(),
    ),
)
@pytest.mark.parametrize(
    "value", (123, False, "shit", {"a": "b"}, ascii_letters.split())
)
def test_defaults(app, key, value):
    app.config[CONSTANCE_SETTINGS][key] = value
    assert getattr(config, key) == value
