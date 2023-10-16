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

    # Authentication
    AUTH_USER_MODEL = 'static_site.User'

    @staticmethod
    def apply(settings: Settings) -> None:
        service = Service('postgres-static')
        settings['DATABASES']['default']['PORT'] = service.container_port('5432/tcp')
        settings['INSTALLED_APPS'] += ['tests.static_site']
