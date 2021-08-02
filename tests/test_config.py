import random
from string import ascii_letters

import pytest

from flask_constance import config
from flask_constance.const import CONSTANCE_SETTINGS


def genstr(n: int = 8):
    return "".join(random.choice(ascii_letters) for _ in range(n))


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
