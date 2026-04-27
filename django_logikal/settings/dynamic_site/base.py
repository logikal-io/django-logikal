import json
from typing import Any

from django.utils.csp import CSP
from logikal_utils.imports import installed
from logikal_utils.project import tool_config
from stormware.amazon.auth import AWSAuth
from stormware.google.secrets import SecretManager

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
        'django.middleware.csp.ContentSecurityPolicyMiddleware',  # CSP header and nonce support
    ]

    # Security
    SECURE_CSP = {'default-src': [CSP.SELF, CSP.NONCE]}
    SECURE_REFERRER_POLICY = ['same-origin', 'origin-when-cross-origin']
    SESSION_COOKIE_AGE = 7 * 24 * 60 * 60  # 7 days (default: 14 days)

    # Internationalization
    LANGUAGE_COOKIE_NAME = 'language'
    LANGUAGE_COOKIE_SAMESITE = 'Lax'

    # Authentication
    LOGIN_URL = 'admin:login'
    LOGIN_REDIRECT_URL = 'admin:index'
    LOGOUT_REDIRECT_URL = 'admin:login'
    AUTH_MIN_PASSWORD_LENGTH = 10
    AUTH_PASSWORD_VALIDATORS = [{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': AUTH_MIN_PASSWORD_LENGTH},
    }]
    PASSWORD_RESET_TIMEOUT = 1 * 24 * 60 * 60  # 1 day (default: 3 days)
    ALLAUTH_SOCIAL_PROVIDER_SECRET_PATH_PREFIX = 'auth-secret'

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
    def _configure_auth(cls, settings: Settings) -> None:
        # Update Django auth settings
        settings.setdefault('ACCOUNT_TEMPLATE_EXTENSION', 'html.j')
        if settings['ACCOUNT_TEMPLATE_EXTENSION'] == 'html.j':
            settings['ACCOUNT_ADAPTER'] = 'django_logikal.auth.AccountAdapter'
            settings['ACCOUNT_FORMS'] = {
                'signup': 'allauth.account.forms.SignupForm',
                'set_password': 'django_logikal.forms.account.SetPasswordForm',
                'change_password': 'django_logikal.forms.account.ChangePasswordForm',
            }
            settings['LOGIN_URL'] = 'account_auth'
            settings['LOGIN_REDIRECT_URL'] = 'account'
            settings['LOGOUT_REDIRECT_URL'] = 'account_auth'
        else:
            settings['LOGIN_URL'] = 'account_login'
            settings['LOGIN_REDIRECT_URL'] = 'socialaccount_connections'
            settings['LOGOUT_REDIRECT_URL'] = 'account_login'

        # See https://docs.allauth.org/en/dev/installation/quickstart.html
        backend = 'allauth.account.auth_backends.AuthenticationBackend'
        settings['AUTHENTICATION_BACKENDS'] = [backend]
        cls.extend(settings['INSTALLED_APPS'], ['allauth', 'allauth.account'])
        cls.append(settings['MIDDLEWARE'], 'allauth.account.middleware.AccountMiddleware')

        # Allauth: overall
        settings['ACCOUNT_SESSION_REMEMBER'] = True

        # Allauth: signup
        settings['ACCOUNT_SIGNUP_FIELDS'] = ['email*', 'password1*']

        # Allauth: login
        settings['ACCOUNT_LOGIN_METHODS'] = {'email'}

        # Allauth: email verification
        settings['ACCOUNT_CONFIRM_EMAIL_ON_GET'] = True
        settings['ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS'] = 1
        settings['ACCOUNT_EMAIL_VERIFICATION'] = 'mandatory'

        # Allauth: user model
        settings['ACCOUNT_USER_MODEL_USERNAME_FIELD'] = None

        # Allauth: social account providers
        auth_config = tool_config('django_logikal').get('auth', {})
        settings['ALLAUTH_SOCIAL_PROVIDERS'] = auth_config.get('social_providers', {})
        if not settings['ALLAUTH_SOCIAL_PROVIDERS']:
            return

        cls.append(settings['INSTALLED_APPS'], 'allauth.socialaccount')
        settings['SOCIALACCOUNT_ADAPTER'] = 'django_logikal.auth.SocialAccountAdapter'
        settings['SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT'] = True
        settings['SOCIALACCOUNT_PROVIDERS'] = {}
        with SecretManager() as secrets:
            for provider_module, provider in settings['ALLAUTH_SOCIAL_PROVIDERS'].items():
                provider_package = f'allauth.socialaccount.providers.{provider_module}'
                if not installed(provider_package):
                    raise RuntimeError(f'Invalid auth provider "{provider_module}"')

                cls.append(settings['INSTALLED_APPS'], provider_package)
                secret_path = '-'.join([
                    settings['SECRET_PATH_PREFIX'],
                    settings['ALLAUTH_SOCIAL_PROVIDER_SECRET_PATH_PREFIX'],
                    provider_module,
                ])
                settings['SOCIALACCOUNT_PROVIDERS'][provider_module] = json.loads(
                    secrets[secret_path],
                )

    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.extend(settings['INSTALLED_APPS'], [
            'django.contrib.admin',
            'django.contrib.messages',  # required by Django admin and django-allauth
            'django.contrib.sessions',  # required by Django admin
            'anymail',
        ])

        if installed('allauth'):
            cls._configure_auth(settings)

        if installed('django_htmx'):
            # See https://django-htmx.readthedocs.io/en/latest/installation.html
            cls.append(settings['INSTALLED_APPS'], 'django_htmx')
            cls.append(settings['MIDDLEWARE'], 'django_htmx.middleware.HtmxMiddleware')
