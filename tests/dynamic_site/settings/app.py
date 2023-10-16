from django.utils.translation import gettext_lazy as _

from django_logikal.settings import Settings, SettingsUpdate


class AppSettings(SettingsUpdate):
    # Core settings
    ROOT_URLCONF = 'tests.dynamic_site.urls'

    # Internationalization
    LANGUAGES = [
        ('en-us', _('English (United States)')),
        ('en-gb', _('English (United Kingdom)')),
    ]

    # Authentication
    AUTH_USER_MODEL = 'dynamic_site.User'
    LOGOUT_REDIRECT_URL = 'dynamic_site:index'

    # Email
    EMAIL_SUBJECT_PREFIX = '[Dynamic Site]'

    # Bibliography
    BIBLIOGRAPHIES = {'references': 'dynamic_site/references.bib'}

    @staticmethod
    def apply(settings: Settings) -> None:
        settings['INSTALLED_APPS'] += ['tests.dynamic_site']
        settings['ANYMAIL']['AMAZON_SES_SESSION_PARAMS']['region_name'] = 'eu-central-1'
