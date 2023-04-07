import typing as t

from flask import Flask

from . import signals
from .backends import Backend, BackendCache
from .storage import Storage
from .backends.memory import MemoryBackend


class Constance:
    """Constance extension

    :param app: Flask application.
    :param backend: Backend instance to use.
    """

    def __init__(
        self,
        app: t.Optional[Flask] = None,
        backend: t.Optional[Backend] = None,
        cache: t.Optional[BackendCache] = None,
    ):
        self.storage: Storage = (
            Storage(backend, cache) if backend else Storage(MemoryBackend(), cache)
        )
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize extension with Flask application.

        :param app: Flask application.
        :raises ConstanceAlreadyInitializedError: If Constance extension
            was already initialized.
        :raises ConstanceInvalidSettingName: If invalid settings name was provided.
        """
        if "constance" in app.extensions:
            raise RuntimeError("Flask-Constance already initialized.")
        app.extensions["constance"] = self
        app.config.setdefault("CONSTANCE_PAYLOAD", {})
        for key in app.config["CONSTANCE_PAYLOAD"].keys():
            if key.startswith("_") or key == "mut":
                raise ValueError(f"Invalid setting name: {key}")
        signals.constance_setup.send(self, app=app)
