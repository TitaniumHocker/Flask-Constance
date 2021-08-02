import pickle
import typing as t

try:
    import redis
except ImportError as exc:
    raise ImportError("To use Redis backen redis-py need to be installed.") from exc

from .core import Backend


class RedisBackend(Backend):
    """Redis backend

    :param URL: Connection URL.
    :param prefix: Prefix to use.
        By default - `constance_settings`."""

    def __init__(self, URL: str, prefix: str = "constance_settings"):
        self.redis = redis.from_url(URL)
        self.prefix = prefix

    def get(self, key: str) -> t.Any:
        value = self.redis.get(f"{self.prefix}:{key}")
        if not value:
            return None
        return pickle.loads(value)

    def set(self, key: str, value: t.Any) -> t.Any:
        old = self.get(key)
        self.redis.set(f"{self.prefix}:{key}", pickle.dumps(value))
        return old
