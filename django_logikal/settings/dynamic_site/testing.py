from django_logikal.settings import Settings
from django_logikal.settings.common.testing import CommonTestingSettings
from django_logikal.settings.dynamic_site.dev import DevSettings


class TestingSettings(CommonTestingSettings, DevSettings):
    """
    Standard settings for testing dynamic sites.
    """
    @staticmethod
    def apply(settings: Settings) -> None:
        settings['MIDDLEWARE'] = [
            middleware for middleware in settings['MIDDLEWARE']
            if 'WhiteNoiseMiddleware' not in middleware
        ]
