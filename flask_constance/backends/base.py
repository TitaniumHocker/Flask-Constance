import typing as t


class Backend(t.Protocol):
    """Base backend class."""

    def get(self, name: str) -> t.Any:
        ...

    def set(self, name: str, value: t.Any) -> None:
        ...


class BackendCache(t.Protocol):
    """Base backend cache class."""

    def get(self, name: str) -> t.Any:
        ...

    def set(self, name: str, value: t.Any) -> None:
        ...

    def invalidate(self, name: str) -> None:
        ...
