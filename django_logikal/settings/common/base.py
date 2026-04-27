import logging
import os
from pathlib import Path

from django.utils.translation import gettext_lazy
from logikal_utils.project import PYPROJECT

from django_logikal.settings import Settings, SettingsUpdate


class CommonBaseSettings(SettingsUpdate):
    ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']  # variants of localhost
    INSTALLED_APPS = [
        'django.contrib.auth',  # required by sites, Django admin and allauth
        'django.contrib.contenttypes',  # required by sites and Django admin
        'django.contrib.sites',  # needed for the sitemap and the robots application
        'django.contrib.sitemaps',
        'django.contrib.staticfiles',
        'robots',
        'django_logikal',
    ]
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django_logikal.static.ManifestStaticFilesStorage'},
    }
    TEMPLATES = [{
        'BACKEND': 'django_logikal.templates.jinja.JinjaTemplates',
        'APP_DIRS': True,
    }, {
        # Needed for the bibliography module (and Django admin)
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # needed for Django admin
                'django.template.context_processors.csp',  # needed for Django admin overrides
                'django.contrib.auth.context_processors.auth',  # needed for Django admin & allauth
                'django.contrib.messages.context_processors.messages',  # needed for Django admin
            ],
        },
    }]
    SITE_ID = 1  # ID of the site created by default
    ROBOTS_SITEMAP_VIEW_NAME = 'sitemap'

    # Static files
    STATIC_ROOT = Path(os.getcwd()) / 'static'
    STATIC_URL = '/static/'

    # Internationalization
    LANGUAGES = [('en-us', gettext_lazy('English (United States)'))]
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'Europe/Zurich'

    # Secrets
    SECRET_PATH_PREFIX = PYPROJECT['project']['name']

    @staticmethod
    def apply(settings: Settings) -> None:
        # Logging
        logging.captureWarnings(capture=True)
        logging.getLogger('blib2to3').setLevel(logging.WARNING)  # Black migration formatting
