import inspect
from typing import Any, Dict, Type

from django_logikal.env import get_option


class SettingsUpdateMeta(type):
    def __str__(cls) -> str:
        return f'{cls.__module__}.{cls.__qualname__}'


class SettingsUpdate(metaclass=SettingsUpdateMeta):
    @staticmethod
    def apply(settings: 'Settings') -> None:
        """
        Apply the current settings update to the provided settings.
        """


class Settings:
    def __init__(self, settings: Dict[str, Any]):
        """
        Store and update the provided settings.
        """
        self._settings = settings

    def __setitem__(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._settings[key]

    def __contains__(self, item: str) -> bool:
        return item in self._settings

    def update(self, settings_update: Type[SettingsUpdate]) -> 'Settings':
        """
        Apply the given settings update to the stored settings.
        """
        # Apply updates from class attributes
        if get_option('log_level') == 'DEBUG':
            print(f'Settings update: {settings_update}')
        for attribute in dir(settings_update):
            if attribute == attribute.upper():
                self[attribute] = getattr(settings_update, attribute)

        # Apply dynamic updates from the entire class inheritance tree (starting at the root)
        for base in reversed(inspect.getmro(settings_update)):
            # Note: we only call apply when it is not inherited
            # (because we will walk up the inheritance tree anyways)
            if issubclass(base, SettingsUpdate) and 'apply' in base.__dict__:
                if get_option('log_level') == 'DEBUG':
                    print(f'Applying {base}')
                base.apply(self)

        return self
