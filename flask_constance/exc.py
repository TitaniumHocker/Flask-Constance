class ConstanceException(Exception):
    """Base constance exception."""


class ConstanceNotInitializedError(ConstanceException):
    """Flask-Constance extension wasn't initialized."""

    def __init__(self):
        super().__init__(self.__doc__)


class ConstanceAlreadyInitializedError(ConstanceException):
    """Flask-Constance extension already initialized."""

    def __init__(self):
        super().__init__(self.__doc__)


class ConstanceSettingNotFoundError(ConstanceException):
    """Setting not found."""

    def __init__(self, name: str):
        super().__init__(f"Setting '{name}' not found.")


class ConstanceInvalidSettingName(ConstanceException):
    """Invalid setting name."""

    def __init__(self, name: str):
        super().__init__(f"Setting name '{name}' is invalid. It's can't begin with underscore.")
