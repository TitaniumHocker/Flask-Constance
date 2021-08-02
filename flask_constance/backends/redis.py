import pickle
import typing as t

try:
    import redis
except ImportError as exc:
    raise ImportError("To use Redis backen redis-py need to be installed.") from exc

from .core import Backend


class RedisBackend(Backend):
    """Redis backend

    :param URL: Connection URL or Redis client instance.
    :param prefix: Prefix to use.
        By default - `constance_settings`.
    """

    def __init__(
        self, connection: t.Union[str, redis.Redis], prefix: str = "constance_settings"
    ):
        if isinstance(connection, str):
            self.redis = redis.from_url(connection)
        else:
            self.redis = connection
        self.prefix = prefix

    def get(self, key: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        value = self.redis.get(f"{self.prefix}:{key}")
        if not value:
            return None
        return pickle.loads(value)

    def set(self, key: str, value: t.Any) -> t.Any:
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        :returns: Old value of the setting.
        """
        old = self.get(key)
        self.redis.set(f"{self.prefix}:{key}", pickle.dumps(value))
        return old
