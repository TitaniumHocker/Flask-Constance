import typing as t

from flask import current_app, g

from .backends import Backend, BackendCache
from .signals import constance_get, constance_set


class Storage:
    """Flask-Constance settings storage.

    This is access point for getting and setting constance settings.

    :param backend: Backend instance to use. By default is Memory backend.
    :param cache: Caching backend to use. This is optional.
    """

    # NOTE: This hack prevents setting undeclared constance settings.
    __slots__ = ["_backend", "_cache"]

    def __init__(self, backend: Backend, cache: t.Optional[BackendCache] = None):
        self._backend: Backend = backend
        self._cache: t.Optional[BackendCache] = cache

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

    @property
    def _mut_log(self) -> t.Dict[str, t.Any]:
        """Mutations log with name of the setting and it's value."""
        if not hasattr(g, "_constance_mut_watchdog"):
            g._constance_mut_watchdog = {}
        return g._constance_mut_watchdog

    def __dir__(self) -> t.Iterable[str]:
        return tuple(self._payload.keys())

    def __getattr__(self, name: str) -> t.Any:
        if name not in self._payload:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        constance_get.send(self, name=name)

        # First of all - try to get value from runtime cache.
        if name in self._ctx_cache:
            return self._ctx_cache[name]

        # Then try to find value in backend cache.
        if self._cache is not None:
            try:
                value = self._cache.get(name)
            except KeyError:
                pass
            else:
                self._ctx_cache[name] = value
                return value

        # Finally go to the actual backend.
        try:
            value = self._backend.get(name)
        except KeyError:
            value = self._payload[name]
            self._backend.set(name, value)
            if self._cache is not None:
                self._cahce.set(name, value)
            self._ctx_cache[name] = value
            if isinstance(value, (dict, list, set)):
                self._mut_log[name] = value
            return value
        else:
            if self._cache is not None:
                self._cache.set(name, value)
            self._ctx_cache[name] = value
            if isinstance(value, (dict, list, set)):
                self._mut_log[name] = value
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

    def __delattr__(self, name: str) -> None:
        if name in self.__slots__:
            return super().__delattr__(name)
        if name not in self._payload:
            return super().__delattr__(name)
        return self.__setattr__(name, self._payload[name])
