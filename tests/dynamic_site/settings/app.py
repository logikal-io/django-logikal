from pathlib import Path

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

    # Email
    EMAIL_SUBJECT_PREFIX = '[Dynamic Site]'

    # Bibliography
    BIBLIOGRAPHIES = {'references': 'dynamic_site/references.bib'}

    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.extend(settings['INSTALLED_APPS'], ['rest_framework', 'tests.dynamic_site'])
        settings['ANYMAIL']['AMAZON_SES_SESSION_PARAMS']['region_name'] = 'eu-central-1'
        settings['TEMPLATES'][1]['DIRS'] = [str(Path(__file__).parents[1] / 'templates')]
