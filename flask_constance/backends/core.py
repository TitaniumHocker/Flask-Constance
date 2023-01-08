import typing as t


class Backend(t.Protocol):
    """Base backend class."""

    def get(self, name: str) -> t.Any:
        ...

    def set(self, name: str, value: t.Any):
        ...
