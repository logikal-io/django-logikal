from django_logikal.env import option_is_set
from django_logikal.settings import Settings
from django_logikal.settings.common.dev import CommonDevSettings
from django_logikal.settings.dynamic_site.base import BaseSettings


class DevSettings(CommonDevSettings, BaseSettings):
    """
    Standard settings for developing dynamic sites.
    """
    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.insert_before(
            setting=settings['INSTALLED_APPS'],
            value='whitenoise.runserver_nostatic',
            before='django.contrib.staticfiles',
        )
        if not option_is_set('send_emails'):
            settings['EMAIL_BACKEND'] = 'django.core.mail.backends.console.EmailBackend'
