import json
from importlib import import_module

from pytest_mock import MockerFixture


def test_dev_settings() -> None:
    secret_key = 'dev'  # nosec: only used for this test
    dev = import_module('tests.dynamic_site.settings.dev')
    assert dev.SECRET_KEY == secret_key
    assert dev.DATABASES['default']['HOST'] == '127.0.0.1'
    assert 'django_logikal.validation.ValidationMiddleware' in dev.MIDDLEWARE
    assert 'console.EmailBackend' in dev.EMAIL_BACKEND


def test_production_settings(mocker: MockerFixture) -> None:
    mocker.patch('stormware.google.auth.GCPAuth')
    cloud_logging_client = mocker.patch('django_logikal.logging.cloud_logging.Client')
    database_secrets = {
        'hostname': 'test_hostname',
        'port': 'test_port',
        'database': 'test_database',
        'username': 'test_username',
        'password': 'test_password',  # nosec: only used for testing
    }
    secret_key = 'production'  # nosec: only used for this test
    secret_manager = mocker.patch('stormware.google.secrets.SecretManager')
    secret_manager.return_value.__enter__.return_value = {
        'website-secret-key': secret_key,
        'website-database-access': json.dumps(database_secrets),
    }
    production = import_module('tests.dynamic_site.settings.production')
    assert production.SECRET_KEY == secret_key
    assert production.DATABASES['default']['HOST'] == database_secrets['hostname']
    assert cloud_logging_client.called
