from flask.globals import _lookup_app_object
from werkzeug.local import LocalProxy

from .const import CONSTANCE_EXTENSION

config = LocalProxy(lambda: _lookup_app_object("app").extensions[CONSTANCE_EXTENSION].config)
