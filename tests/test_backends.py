import pickle

import pytest

from conftest import genstr


def test_dummy_backend(dummy_backend):
    with pytest.raises(NotImplementedError):
        dummy_backend.get("a")
    with pytest.raises(NotImplementedError):
        dummy_backend.set("a", 1)


@pytest.mark.parametrize("key", (genstr() for _ in range(3)))
@pytest.mark.parametrize("value", (True, False, 123, "awdawd", [1, 2, 3]))
def test_memory_backend(memory_backend, key, value):
    assert memory_backend.get(key) is None
    assert key not in memory_backend._db
    assert memory_backend.set(key, value) is None
    assert memory_backend.get(key) == value
    assert memory_backend._db[key] == value
    assert memory_backend.set(key, 1) == value


@pytest.mark.parametrize("key", (genstr() for _ in range(3)))
@pytest.mark.parametrize("value", (True, False, 123, "awdawd", [1, 2, 3]))
def test_fsqla_backend(fsqla_backend, key, value):
    assert fsqla_backend.get(key) is None
    assert fsqla_backend.model.query.filter_by(key=key).first() is None
    assert fsqla_backend.set(key, value) is None
    assert fsqla_backend.get(key) == value
    assert pickle.loads(fsqla_backend.model.query.filter_by(key=key).first().value) == value
    assert fsqla_backend.set(key, 1) == value


@pytest.mark.parametrize("key", (genstr() for _ in range(3)))
@pytest.mark.parametrize("value", (True, False, 123, "awdawd", [1, 2, 3]))
def test_redis_backend(redis_backend, key, value):
    assert redis_backend.get(key) is None
    assert redis_backend.redis.get(f"{redis_backend.prefix}:{key}") is None
    assert redis_backend.set(key, value) is None
    assert redis_backend.get(key) == value
    assert pickle.loads(redis_backend.redis.get(f"{redis_backend.prefix}:{key}")) == value
    assert redis_backend.set(key, 1) == value
