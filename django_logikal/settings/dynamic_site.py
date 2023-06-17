# pylint: disable=wildcard-import, unused-wildcard-import
from typing import Any, Dict

from stormware.amazon.auth import AWSAuth

from django_logikal.env import option_is_set
from django_logikal.settings.base import *

# Security
SECRET_KEY = 'local'  # nosec: only used for local development and testing

# Core settings
INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.messages',  # required by Django admin
    'django.contrib.sessions',  # required by Django admin
    'anymail',
]
MIDDLEWARE = [
    *[middleware for middleware in MIDDLEWARE if 'DebugToolbarMiddleware' in middleware],
    'django.middleware.security.SecurityMiddleware',  # required for HTTPS redirection and others
    'django.contrib.sessions.middleware.SessionMiddleware',  # required by Django admin
    'django.middleware.locale.LocaleMiddleware',  # required for localization
    'django.middleware.common.CommonMiddleware',  # performs URL rewriting and sets headers
    'django.middleware.csrf.CsrfViewMiddleware',  # adds hidden form fields to POST forms
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # required by Django admin
    'django_logikal.security.LoginRequiredByDefaultMiddleware',  # force login by default
    'django.contrib.messages.middleware.MessageMiddleware',  # required by Django admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # defense against clickjacking
    *[
        middleware for middleware in MIDDLEWARE
        if 'DebugToolbarMiddleware' not in middleware
        and middleware not in (  # these are re-inserted at the correct position
            'django.middleware.common.CommonMiddleware',
            'django.middleware.locale.LocaleMiddleware',
        )
    ],
]

# Security
SECURE_REFERRER_POLICY = ['same-origin', 'origin-when-cross-origin']
SESSION_COOKIE_AGE = 7 * 24 * 60 * 60  # 7 days (default: 14 days)

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

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_TIMEOUT = 10  # default: infinite
ANYMAIL: Dict[str, Any] = {
    'REQUESTS_TIMEOUT': 10,  # default: 30s
    'AMAZON_SES_SESSION_PARAMS': {'profile_name': AWSAuth().profile()},
}
if option_is_set('toolbar'):  # pragma: no cover, tested in subprocess
    DEBUG_TOOLBAR_PANELS = ['mail_panel.panels.MailToolbarPanel', *DEBUG_TOOLBAR_PANELS]
    EMAIL_BACKEND = 'mail_panel.backend.MailToolbarBackend'
    INSTALLED_APPS += ['mail_panel']
elif option_is_set('send_emails'):  # pragma: no cover, tested with production settings
    EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'
