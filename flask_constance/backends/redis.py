import pickle
import typing as t

try:
    import redis
except ImportError as err:
    raise ImportError("To use Redis backen redis-py need to be installed.") from err

from .core import Backend
from . import exc


class RedisBackend(Backend):
    """Redis backend

    :param URL: Connection URL or Redis client instance.
    :param prefix: Prefix to use.
        By default - `constance_settings`.
    """

    def __init__(self, connection: t.Union[str, redis.Redis], prefix: str = "constance_settings"):
        if isinstance(connection, str):
            self.redis = redis.from_url(connection)
        else:
            self.redis = connection
        self.prefix = prefix

    def get(self, name: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        value = self.redis.get(f"{self.prefix}:{name}")
        if not value:
            raise exc.SettingNotFoundInBackendError(name, self)
        return pickle.loads(value)

    def set(self, key: str, value: t.Any) -> t.Any:
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        """
        self.redis.set(f"{self.prefix}:{key}", pickle.dumps(value))
