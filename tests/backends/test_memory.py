import pytest

from flask_constance.backends.memory import MemoryBackend, MemoryBackendCache


@pytest.fixture
def memory_backend():
    return MemoryBackend()


@pytest.fixture
def memory_backend_cache():
    return MemoryBackendCache()


@pytest.mark.parametrize("key", ("abc", "bca", "foo", "bar"))
@pytest.mark.parametrize("value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_setget(memory_backend: MemoryBackend, key, value):
    memory_backend.set(key, value)
    assert memory_backend.get(key) == value
    assert getattr(memory_backend._db, key) == value


@pytest.mark.parametrize("key", ("abc", "bca", "foo", "bar"))
@pytest.mark.parametrize("value", ("value", True, None, [4, 2], 13, {"foo": "bar"}))
def test_setget_cache(memory_backend_cache: MemoryBackendCache, key, value):
    memory_backend_cache.set(key, value)
    assert memory_backend_cache.get(key) == value
    assert getattr(memory_backend_cache._db, key) == value
    memory_backend_cache.invalidate(key)
    with pytest.raises(KeyError):
        memory_backend_cache.get(key)
