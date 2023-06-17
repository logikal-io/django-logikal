# pylint: disable=wildcard-import, unused-wildcard-import
from django.utils.translation import gettext_lazy as _

from django_logikal.settings.dynamic_site import *

# Core settings
INSTALLED_APPS += ['tests.dynamic_site']
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
ANYMAIL['AMAZON_SES_SESSION_PARAMS']['region_name'] = 'eu-central-1'

# Bibliography
BIBLIOGRAPHIES = {'references': 'dynamic_site/references.bib'}
