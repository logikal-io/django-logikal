from django_logikal.settings import Settings
from django_logikal.settings.common.dev import CommonDevSettings
from django_logikal.settings.static_site.base import BaseSettings


class DevSettings(CommonDevSettings, BaseSettings):
    """
    Standard settings for developing static sites.
    """
    @staticmethod
    def apply(settings: Settings) -> None:
        pass
