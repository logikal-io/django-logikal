import logging
import os
from importlib.util import find_spec
from pathlib import Path

from django.utils.translation import gettext_lazy
from pytest_logikal.docker import Service

from django_logikal.env import get_option, option_is_set
from django_logikal.logging import logging_config

# Logging
logging.captureWarnings(capture=True)
logging.getLogger('blib2to3').setLevel(logging.WARNING)  # used during Black migration formatting

LOGGING = logging_config(
    log_level=get_option('log_level', 'INFO'),
    console=True,
    cloud=option_is_set('cloud_logging'),
)

# Core settings
DEBUG = option_is_set('local_run')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'PORT': Service('postgres').container_port('5432/tcp'),
        'NAME': 'local',
        'USER': 'local',
        'PASSWORD': 'local',
    },
}
MIGRATION_LINTER_OPTIONS = {
    'exclude_apps': ['sites', 'robots'],
}
# Note: we cannot use UUID fields as a default yet, see https://code.djangoproject.com/ticket/32577
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INSTALLED_APPS = [
    'django.contrib.auth',  # required by sites, Django admin and for the auth framework
    'django.contrib.contenttypes',  # required by sites, Django admin and for the auth framework
    'django.contrib.sites',  # needed for the sitemap and the robots application
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'robots',
    'django_logikal',
]
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',  # required for localization
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',  # adds site attribute to requests
    'django_logikal.validation.ValidationMiddleware',  # HTML validation
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
            'django.template.context_processors.request',  # required by Django admin
            'django.contrib.auth.context_processors.auth',  # required by Django admin
            'django.contrib.messages.context_processors.messages',  # required by Django admin
        ],
    },
}]
SITE_ID = 1  # ID of the site created by default
ROBOTS_SITEMAP_VIEW_NAME = 'sitemap'

# Static files
STATIC_ROOT = Path(os.getcwd()) / 'static'
STATIC_URL = '/static/'

# Internationalization
USE_I18N = True
LANGUAGES = [('en-us', gettext_lazy('English (United States)'))]
LANGUAGE_CODE = 'en-us'
USE_TZ = True
TIME_ZONE = 'Europe/Zurich'

# Migration linter
if find_spec('django_migration_linter'):
    INSTALLED_APPS += ['django_migration_linter']
    MIGRATION_LINTER_OVERRIDE_MAKEMIGRATIONS = True

# Debug toolbar
if option_is_set('toolbar'):  # pragma: no cover, tested in subprocess
    INSTALLED_APPS += ['debug_toolbar', 'template_profiler_panel']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', *MIDDLEWARE]
    INTERNAL_IPS = ['127.0.0.1']
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
        'TOOLBAR_LANGUAGE': 'en-us',
        'SQL_WARNING_THRESHOLD': 100,  # milliseconds
        'DISABLE_PANELS': {
            'debug_toolbar.panels.signals.SignalsPanel',
            'debug_toolbar.panels.redirects.RedirectsPanel',
            'debug_toolbar.panels.profiling.ProfilingPanel',
        },
    }
