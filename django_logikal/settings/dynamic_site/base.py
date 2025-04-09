from typing import Any

from csp.constants import NONCE, SELF
from stormware.amazon.auth import AWSAuth

from django_logikal.settings import Settings
from django_logikal.settings.common.base import CommonBaseSettings


class BaseSettings(CommonBaseSettings):
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',  # required for HTTPS redirection & others
        'whitenoise.middleware.WhiteNoiseMiddleware',  # static file serving
        'django.contrib.sessions.middleware.SessionMiddleware',  # required by Django admin
        'django.middleware.locale.LocaleMiddleware',  # required for localization
        'django.middleware.common.CommonMiddleware',  # performs URL rewriting and sets headers
        'django.middleware.csrf.CsrfViewMiddleware',  # adds hidden form fields to POST forms
        'django.contrib.auth.middleware.AuthenticationMiddleware',  # required by Django admin
        'django_logikal.security.LoginRequiredByDefaultMiddleware',  # force login by default
        'django.contrib.messages.middleware.MessageMiddleware',  # required by Django admin
        'django.contrib.sites.middleware.CurrentSiteMiddleware',  # adds site attribute to requests
        'django.middleware.clickjacking.XFrameOptionsMiddleware',  # defense against clickjacking
        'csp.middleware.CSPMiddleware',  # adds the Content-Security-Policy header
    ]

    # Security
    SECURE_REFERRER_POLICY = ['same-origin', 'origin-when-cross-origin']
    SESSION_COOKIE_AGE = 7 * 24 * 60 * 60  # 7 days (default: 14 days)
    CONTENT_SECURITY_POLICY = {
        'DIRECTIVES': {'default-src': [SELF, NONCE]},
    }

    # Internationalization
    LANGUAGE_COOKIE_NAME = 'language'
    LANGUAGE_COOKIE_SAMESITE = 'Lax'

    # Authentication
    LOGIN_URL = 'admin:login'
    LOGIN_REDIRECT_URL = 'admin:index'
    LOGOUT_REDIRECT_URL = 'admin:login'
    AUTH_MIN_PASSWORD_LENGTH = 8
    AUTH_PASSWORD_VALIDATORS = [{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': AUTH_MIN_PASSWORD_LENGTH},
    }]
    PASSWORD_RESET_TIMEOUT = 1 * 24 * 60 * 60  # 1 day (default: 3 days)

    # API
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication'],
        'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    }

    # Email
    EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'
    EMAIL_TIMEOUT = 10  # default: infinite
    ANYMAIL: dict[str, Any] = {
        'REQUESTS_TIMEOUT': 10,  # default: 30s
        'AMAZON_SES_SESSION_PARAMS': {'profile_name': AWSAuth().profile()},
    }

    # Static files
    STORAGES = {**CommonBaseSettings.STORAGES, **{
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }}
    WHITENOISE_KEEP_ONLY_HASHED_FILES = True

    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.extend(settings['INSTALLED_APPS'], [
            'django.contrib.admin',
            'django.contrib.messages',  # required by Django admin
            'django.contrib.sessions',  # required by Django admin
            'anymail',
            'csp',
        ])
