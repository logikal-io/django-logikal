import os
from pathlib import Path

from django_logikal.settings import Settings
from django_logikal.settings.common.base import CommonBaseSettings


class BaseSettings(CommonBaseSettings):
    MIDDLEWARE = [
        'django.middleware.locale.LocaleMiddleware',  # required for localization
        'django.middleware.common.CommonMiddleware',  # performs URL rewriting and sets headers
        'django.contrib.sites.middleware.CurrentSiteMiddleware',  # adds site attribute to requests
    ]

    # Static site generation
    DISTILL_DIR = Path(os.getcwd()) / 'generated'

    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.append(settings['INSTALLED_APPS'], 'django_distill')
