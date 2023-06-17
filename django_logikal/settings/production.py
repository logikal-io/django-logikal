# pylint: disable=wildcard-import, unused-wildcard-import
import json

from stormware.google.secrets import SecretManager

from django_logikal.logging import logging_config
from django_logikal.settings.dynamic_site import *

# Logging
LOGGING = logging_config(console=False, cloud=True)

# Security
with SecretManager() as secrets:
    SECRET_KEY = secrets['django-secret-key']
    database_secrets = json.loads(secrets['django-database-secrets'])

# Core settings
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': database_secrets['hostname'],
        'PORT': database_secrets['port'],
        'NAME': database_secrets['database'],
        'USER': database_secrets['username'],
        'PASSWORD': database_secrets['password'],
    },
}
CONN_MAX_AGE = 1 * 60 * 60  # 1 hour
CONN_HEALTH_CHECKS = True

INSTALLED_APPS = [
    app for app in INSTALLED_APPS
    if app != 'django_migration_linter'
]
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE
    if middleware != 'django_logikal.validation.ValidationMiddleware'
]

# Security
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# Email
EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'
