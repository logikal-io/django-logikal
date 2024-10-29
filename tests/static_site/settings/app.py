from django.utils.translation import gettext_lazy as _
from logikal_utils.docker import Service

from django_logikal.settings import Settings, SettingsUpdate


class AppSettings(SettingsUpdate):
    # Core settings
    ROOT_URLCONF = 'tests.static_site.urls'

    # Internationalization
    LANGUAGES = [
        ('en-us', _('English (United States)')),
        ('en-gb', _('English (United Kingdom)')),
    ]
    DISTILL_LANGUAGES = ['en-us', 'en-gb']  # see https://github.com/meeb/django-distill/issues/80

    # Authentication
    AUTH_USER_MODEL = 'static_site.User'

    @classmethod
    def apply(cls, settings: Settings) -> None:
        service = Service('postgres-static')
        settings['DATABASES']['default']['PORT'] = service.container_port('5432/tcp')
        cls.append(settings['INSTALLED_APPS'], 'tests.static_site')
