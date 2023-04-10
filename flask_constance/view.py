import typing as t

from flask import abort, request
from flask.views import MethodView

from .globals import settings


class ConstanceView(MethodView):
    """Method view for managing dynamic settings."""

    def put(self, name: str):
        """Update value for the setting."""
        if name not in dir(settings):
            abort(404)
        data = request.get_json()
        setattr(settings, name, data)
        return {}, 200

    def get(self, name: t.Optional[str] = None):
        """Get specific setting or all settings."""
        if name:
            if name not in dir(settings):
                abort(404)
            return {name: getattr(settings, name)}
        return {key: getattr(settings, key) for key in dir(settings)}

    def delete(self, name: str):
        """Delete(actually reset) setting value."""
        if name not in dir(settings):
            abort(404)
        delattr(settings, name)
        return {}, 200
