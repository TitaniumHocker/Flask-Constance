import typing as t
from functools import partial

from flask import current_app, g
from contextlib import contextmanager

from .backends import Backend, BackendCache
from .signals import constance_get, constance_set


@contextmanager  # type: ignore
def _mut_context_manager(storage: "Storage", name: str) -> t.ContextManager[t.Any]:  # type: ignore
    """Context manager for updating muttable values in storage.

    :param storage: Storage.
    :param name: Name of the setting.
    :yields: Context manager returning value of setting.
    """
    value = getattr(storage, name)
    yield value
    setattr(storage, name, value)


class Storage:
    """Flask-Constance settings storage.

    This is access point for getting and setting constance settings.

    :param backend: Backend instance to use. By default is Memory backend.
    :param cache: Caching backend to use. This is optional.
    """

    # NOTE: This hack prevents setting undeclared constance settings.
    __slots__ = ["_backend", "_cache", "_initialized"]

    def __init__(self, backend: Backend, cache: t.Optional[BackendCache] = None):
        self._backend: Backend = backend
        self._cache: t.Optional[BackendCache] = cache
        self._initialized = True

    @property
    def mut(self) -> t.Callable[[str], t.ContextManager[t.Any]]:
        """Context manager to partial updating muttable settings."""
        return partial(_mut_context_manager, self)

    @property
    def _payload(self) -> t.Dict[str, t.Any]:
        """Constance payload. Just proxy to CONSTANCE_PAYLOAD application config variable."""
        return current_app.config["CONSTANCE_PAYLOAD"]

    @property
    def _ctx_cache(self) -> t.Dict[str, t.Any]:
        """Application context cache. This is used to prevent unnessesary lookups to backend."""
        if not hasattr(g, "_constance_runtime_cache"):
            g._constance_runtime_cache = {}
        return g._constance_runtime_cache

    def __dir__(self) -> t.Iterable[str]:
        return tuple(self._payload.keys())

    def __getattr__(self, name: str) -> t.Any:
        if name not in self._payload:
            return super().__getattribute__(name)
        constance_get.send(self, name=name)
        if name in self._ctx_cache:
            return self._ctx_cache[name]
        if self._cache is not None:
            try:
                value = self._cache.get(name)
            except KeyError:
                pass
            else:
                self._ctx_cache[name] = value
                return value
        try:
            value = self._backend.get(name)
        except KeyError:
            value = self._payload[name]
            self._backend.set(name, value)
            if self._cache is not None:
                self._cahce.set(name, value)
            self._ctx_cache[name] = value
            return value
        else:
            if self._cache is not None:
                self._cache.set(name, value)
            self._ctx_cache[name] = value
            return value

    def __setattr__(self, name: str, value: t.Any) -> None:
        if name in self.__slots__:
            return super().__setattr__(name, value)
        if name not in self._payload:
            return super().__setattr__(name, value)
        constance_set.send(self, name=name, value=value)
        self._backend.set(name, value)
        if self._cache is not None:
            self._cache.invalidate(name)
        self._ctx_cache[name] = value
