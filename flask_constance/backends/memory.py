import typing as t
from threading import Lock

from .core import Backend


class MemoryBackend(Backend):
    """In-memory backend for testing purposes"""

    def __init__(self):
        self._lock: Lock = Lock()
        self._db: t.Dict[str, t.Any] = {}

    def get(self, key: str) -> t.Any:
        with self._lock:
            return self._db.get(key)

    def set(self, key: str, value: t.Any) -> t.Any:
        with self._lock:
            old = self._db.get(key)
            self._db[key] = value
        return old
