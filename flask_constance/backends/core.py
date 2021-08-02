import typing as t

from ..signals import constance_get, constance_set


class Backend:
    """Base backend class"""

    def get(self, name: str) -> t.Any:
        """Interface for getting settings"""
        raise NotImplementedError(f"Constance backend({self.__class__}) getter wasn't implemented")

    def _get(self, key: str) -> t.Any:
        """Get setting value.

        :param key: Name of the setting.
        """
        constance_get.send(self, key=key)
        return self.get(key)

    def set(self, key: str, value: t.Any) -> t.Any:
        """Interface for setting settings"""
        raise NotImplementedError(f"Constance backend({self.__class__}) setter wasn't implemented")

    def _set(self, key: str, value: t.Any):
        """Set setting value

        :param key: Name of the setting.
        :param value: Value of the setting.
        :returns: Old value of the setting.
        """
        old = self.set(key, value)
        constance_set.send(self, key=key, value=value, old=old)
        return old
