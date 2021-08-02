import typing as t

from flask import Flask, current_app

from .backends.core import Backend
from .backends.memory import MemoryBackend
from .const import CONSTANCE_EXTENSION, CONSTANCE_SETTINGS
from .signals import constance_setup


class Config:
    """Config object to handle data access

    :param backend: Backend to use.
    """

    def __init__(self, backend: Backend):
        super().__setattr__("_backend", backend)

    def __getattr__(self, key: str) -> t.Any:
        if key not in current_app.config[CONSTANCE_SETTINGS]:
            raise AttributeError(key)
        result = self._backend._get(key)
        if result is None:
            return current_app.config[CONSTANCE_SETTINGS][key]
        return result

    def __setattr__(self, key: str, value: t.Any):
        if key not in current_app.config[CONSTANCE_SETTINGS]:
            raise AttributeError(key)
        self._backend._set(key, value)

    def __dir__(self) -> t.Iterable[str]:
        return current_app.config[CONSTANCE_SETTINGS].keys()


class Constance:
    """Constance extension

    :param app: Flask application.
    :param backend: Backend instance to use.
    """

    def __init__(self, app: t.Optional[Flask] = None, backend: t.Optional[Backend] = None):
        self.config = Config(backend if backend is not None else MemoryBackend())
        self.app: t.Optional[Flask]
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app: Flask):
        """Init Flask application

        :param app: Flask application.
        :raises ValueError: If Constance extension
            was initialized multiple times.
        """
        self.app = app
        if not hasattr(self.app, "extensions"):
            self.app.extensions = {CONSTANCE_EXTENSION: self}
        else:
            if CONSTANCE_EXTENSION in self.app.extensions:
                raise ValueError(
                    f"{CONSTANCE_EXTENSION} extension name already used. " f"Multiple inits?"
                )
            self.app.extensions[CONSTANCE_EXTENSION] = self
        self.app.config.setdefault(CONSTANCE_SETTINGS, {})
        constance_setup.send(self, app=self.app, backend=self.config._backend)
