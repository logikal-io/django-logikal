from django_logikal.env import option_is_set
from django_logikal.settings import Settings
from django_logikal.settings.common.dev import CommonDevSettings
from django_logikal.settings.dynamic_site.base import BaseSettings


class DevSettings(CommonDevSettings, BaseSettings):
    """
    Standard settings for developing dynamic sites.
    """
    @staticmethod
    def apply(settings: Settings) -> None:
        settings['INSTALLED_APPS'].insert(
            settings['INSTALLED_APPS'].index('django.contrib.staticfiles'),
            'whitenoise.runserver_nostatic',
        )

        if not option_is_set('send_emails'):
            settings['EMAIL_BACKEND'] = 'django.core.mail.backends.console.EmailBackend'
