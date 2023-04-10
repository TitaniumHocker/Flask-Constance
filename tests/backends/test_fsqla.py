import typing as t

import pytest

from flask_constance.backends import FlaskSQLAlchemyBackend


@pytest.mark.parametrize("new_value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_setget(
    with_fsqla_backend: FlaskSQLAlchemyBackend,
    default_payload: t.Dict[str, t.Any],
    new_value: t.Any,
):
    # Setup default values as we accessing not throught the global object.
    for key, value in default_payload.items():
        with_fsqla_backend.set(key, value)

    for key, value in default_payload.items():
        assert with_fsqla_backend.get(key) == value
        with_fsqla_backend.set(key, new_value)
        assert with_fsqla_backend.get(key) == new_value
        assert (
            with_fsqla_backend.model.query.filter_by(name=key).first().value
            == new_value
        )
