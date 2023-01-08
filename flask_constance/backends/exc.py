import typing as t

from ..exc import ConstanceException

if t.TYPE_CHECKING:
    from .core import Backend


class ConstanceBackendException(ConstanceException):
    """Base exception for Flask-Constance backends."""


class SettingNotFoundInBackendError(ConstanceBackendException):
    """Setting not found in backend.

    :param name: Name of the setting.
    """

    def __init__(self, name: str, backend: "Backend"):
        super().__init__(f"Setting '{name}' not found in backend '{backend}'.")
