import os
import typing as t

from flask import Flask

from . import signals
from .backends import Backend, BackendCache
from .backends.memory import MemoryBackend
from .cli import cli
from .storage import Storage
from .view import ConstanceView


class Constance:
    """Constance extension

    :param app: Flask application.
    :param backend: Backend instance to use.
    :param backend_cache: Cache for the backend.
    :param view_base_url: Base URL to register REST-like view for settings.
    :param view_class: Class to register as view.
    """

    def __init__(
        self,
        app: t.Optional[Flask] = None,
        backend: t.Optional[Backend] = None,
        cache: t.Optional[BackendCache] = None,
        view_base_url: t.Optional[str] = None,
        view_class: t.Type[ConstanceView] = ConstanceView,
    ):
        self.storage: Storage = (
            Storage(backend, cache) if backend else Storage(MemoryBackend(), cache)
        )
        self.view_base_url = view_base_url
        self.view_class = view_class
        if app is not None:
            self.init_app(app)

    def _teardown(self, err: t.Optional[BaseException]) -> None:
        for name, value in self.storage._mut_log.items():
            setattr(self.storage, name, value)

    def init_app(self, app: Flask) -> None:
        """Initialize extension with Flask application.

        :param app: Flask application.
        :raises RuntimeError: If Constance extension
            was already initialized.
        :raises ValueError: If invalid setting name was provided
            in CONSTANCE_PAYLOAD application config value.
        """
        if "constance" in app.extensions:
            raise RuntimeError("Flask-Constance already initialized.")
        app.extensions["constance"] = self
        app.config.setdefault("CONSTANCE_PAYLOAD", {})
        app.config.setdefault("CONSTANCE_VIEW_BASE_URL", None)
        for key in app.config["CONSTANCE_PAYLOAD"].keys():
            if key.startswith("_") or "-" in key:
                raise ValueError(f"Invalid setting name: {key}")
        app.teardown_appcontext(self._teardown)
        view_base_url = app.config["CONSTANCE_VIEW_BASE_URL"] or self.view_base_url
        if view_base_url is not None:
            self.view = self.view_class.as_view("constance_view")
            app.add_url_rule(
                os.path.join(view_base_url, "<name>"),
                view_func=self.view,
            )
            app.add_url_rule(view_base_url, view_func=self.view)
        app.cli.add_command(cli)
        signals.constance_setup.send(self, app=app)
