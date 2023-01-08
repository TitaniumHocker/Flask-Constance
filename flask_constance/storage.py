import typing as t

from flask import current_app, g

from . import exc
from .backends import Backend, MemoryBackend
from .backends.exc import SettingNotFoundInBackendError
from .signals import constance_get, constance_set


class Storage:
    """Flask-Constance settings storage.

    This is access point for getting and setting constance settings.

    :param backend: Backend instance to use. By default is Memory backend.
    :param cache: Caching backend to use. This is optional.
    """

    # NOTE: This hack prevents setting undeclared constance settings.
    __slots__ = ["_backend", "_cache"]

    def __init__(self, backend: t.Optional[Backend] = None, cache: t.Optional[Backend] = None):
        self._backend: Backend = backend or MemoryBackend()
        self._cache: t.Optional[Backend] = cache

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
        return self._payload.keys()

    def __getattr__(self, name: str) -> t.Any:
        if name not in self._payload:
            raise exc.ConstanceSettingNotFoundError(name)
        constance_get.send(self, name=name)
        if name in self._ctx_cache:
            return self._ctx_cache[name]
        if self._cache is not None:
            try:
                value = self._cache.get(name)
            except SettingNotFoundInBackendError:
                pass
            else:
                self._ctx_cache[name] = value
                return value
        try:
            value = self._backend.get(name)
        except SettingNotFoundInBackendError:
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

    def __setattr__(self, name: str, value: t.Any):
        try:
            if name not in self._payload:
                return super().__setattr__(name, value)
        except RuntimeError:  # NOTE: Prevent falling out while initializing extension.
            return super().__setattr__(name, value)
        constance_set.send(self, name=name, value=value)
        self._backend.set(name, value)
        if self._cache is not None:
            self._cache.set(name, value)
        self._ctx_cache[name] = value
