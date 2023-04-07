import pytest
from flask_constance.backends.memory import MemoryBackend


@pytest.fixture
def memory_backend():
    return MemoryBackend()


@pytest.mark.parametrize("key", ("abc", "bca", "foo", "bar"))
@pytest.mark.parametrize("value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_setget(memory_backend: MemoryBackend, key, value):
    memory_backend.set(key, value)
    assert memory_backend.get(key) == value
    assert getattr(memory_backend._db, key) == value
