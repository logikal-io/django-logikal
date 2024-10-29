import json

from logikal_utils.project import PYPROJECT
from stormware.google.secrets import SecretManager

from django_logikal.logging import logging_config
from django_logikal.settings import Settings, SettingsUpdate


class CommonProductionSettings(SettingsUpdate):
    # Core settings
    DEBUG = False
    CONN_MAX_AGE = 1 * 60 * 60  # 1 hour
    CONN_HEALTH_CHECKS = True

    # Security
    SECRET_KEY_PATH = f'{PYPROJECT['project']['name']}-website-secret-key'  # nosec: this is a path
    DATABASE_SECRETS_PATH = f'{PYPROJECT['project']['name']}-website-database-secrets'

    CSRF_COOKIE_SECURE = True
    LANGUAGE_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    # Email
    EMAIL_BACKEND = 'anymail.backends.amazon_ses.EmailBackend'

    @staticmethod
    def apply(settings: Settings) -> None:
        settings['LOGGING'] = logging_config(console=False, cloud=True)

        with SecretManager() as secrets:
            settings['SECRET_KEY'] = secrets[settings['SECRET_KEY_PATH']]
            database_secrets = json.loads(secrets[settings['DATABASE_SECRETS_PATH']])

        settings['DATABASES'] = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': database_secrets['hostname'],
                'PORT': database_secrets['port'],
                'NAME': database_secrets['database'],
                'USER': database_secrets['username'],
                'PASSWORD': database_secrets['password'],
            },
        }
