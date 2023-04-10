import typing as t

from werkzeug.local import Local

from .base import Backend, BackendCache


class MemoryBackend(Backend):
    """In-memory backend for testing purposes."""

    def __init__(self):
        self._db = Local()

    def get(self, name: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        try:
            return getattr(self._db, name)
        except AttributeError as err:
            raise KeyError(name) from err

    def set(self, name: str, value: t.Any) -> None:
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        """
        setattr(self._db, name, value)


class MemoryBackendCache(MemoryBackend, BackendCache):
    """In-memory backend cache for testing purposes."""

    def invalidate(self, name: str) -> None:
        """Invalidate setting value in cache.

        :param name: Setting name.
        """
        if hasattr(self._db, name):
            delattr(self._db, name)
