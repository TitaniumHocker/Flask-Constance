import pytest
import typing as t
from flask_constance import settings


@pytest.mark.parametrize("new_value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_set(with_memory_backend, default_payload: t.Dict[str, t.Any], new_value: t.Any):
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


def test_dir(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    assert sorted(dir(settings)) == sorted(default_payload.keys())


def test_mut_list(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    for key, value in default_payload.items():
        if isinstance(value, list):
            with settings.mut(key) as muttable:
                muttable.append(123)
            assert getattr(settings, key)[-1] == 123


def test_mut_dict(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    for key, value in default_payload.items():
        if isinstance(value, dict):
            with settings.mut(key) as muttable:
                muttable["qwerty"] = 123
            assert getattr(settings, key)["qwerty"] == 123


def test_mut_set(with_memory_backend, default_payload: t.Dict[str, t.Any]):
    for key, value in default_payload.items():
        if isinstance(value, set):
            with settings.mut(key) as muttable:
                muttable.update("qwerty")
            assert "qwerty" in getattr(settings, key)
