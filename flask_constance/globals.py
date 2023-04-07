from typing import cast

from flask import current_app
from werkzeug.local import LocalProxy

from .storage import Storage


def _get_settings_storage() -> Storage:
    """Flask-Constance settings storage lookup callback.

    :returns: Instance of Flask-Constance's storage.
    :raises ConstanceNotInitializedError: If Flask-Constance wasn't initialized.
    """
    try:
        return cast(Storage, current_app.extensions["constance"].storage)
    except KeyError as err:
        raise RuntimeError("Flask-Constance wasn't initialized.") from err


#: Global variable to access Flask-Constance settings storage.
settings: Storage = cast(Storage, LocalProxy(_get_settings_storage))
