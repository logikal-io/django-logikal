# pylint: disable=wildcard-import, unused-wildcard-import
from django.utils.translation import gettext_lazy as _
from pytest_logikal.docker import Service

from django_logikal.settings.static_site import *

# Core settings
DATABASES['default']['PORT'] = Service('postgres-static').container_port('5432/tcp')
INSTALLED_APPS += ['tests.static_site']
ROOT_URLCONF = 'tests.static_site.urls'

# Internationalization
LANGUAGES = [
    ('en-us', _('English (United States)')),
    ('en-gb', _('English (United Kingdom)')),
]

# Authentication
AUTH_USER_MODEL = 'static_site.User'
