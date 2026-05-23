import json
from importlib import import_module

from logikal_utils.project import PYPROJECT
from pytest import raises
from pytest_mock import MockerFixture

DYNAMIC_SITE_BASE_SECRETS = {
    'django-logikal-auth-secret-google': json.dumps({}),
    'django-logikal-auth-secret-microsoft': json.dumps({}),
}

DATABASE_SECRETS = {
    'hostname': 'test_hostname',
    'port': 'test_port',
    'database': 'test_database',
    'username': 'test_username',
    'password': 'test_password',  # nosec: only used for testing
}

COMMON_PRODUCTION_SECRETS = {
    'django-logikal-secret-key': 'secret-key',  # nosec: only used for testing
    'django-logikal-database-access': json.dumps(DATABASE_SECRETS),
}


def test_settings_errors(mocker: MockerFixture) -> None:
    tool_config = mocker.patch('django_logikal.settings.dynamic_site.base.tool_config')
    tool_config.return_value = {'auth': {'social_providers': {'invalid_provider': 'Invalid'}}}
    with raises(RuntimeError, match='Invalid auth provider'):
        import_module('tests.dynamic_site.settings.dev')


def test_dev_settings(mocker: MockerFixture) -> None:
    mocker.patch.dict(PYPROJECT, {'tool': {'django_logikal': {'auth': {'social_providers': {}}}}})
    dev = import_module('tests.dynamic_site.settings.dev')
    assert dev.SECRET_KEY == 'dev'  # nosec: only an assertion
    assert dev.DATABASES['default']['HOST'] == '127.0.0.1'
    assert 'django_logikal.validation.ValidationMiddleware' in dev.MIDDLEWARE
    assert 'console.EmailBackend' in dev.EMAIL_BACKEND


def test_production_settings(mocker: MockerFixture) -> None:
    mocker.patch('stormware.google.auth.GCPAuth')
    cloud_logging_client = mocker.patch('django_logikal.logging.cloud_logging.Client')
    secret_manager = mocker.patch('django_logikal.settings.common.production.SecretManager')
    secret_manager.return_value.__enter__.return_value = COMMON_PRODUCTION_SECRETS
    secret_manager = mocker.patch('django_logikal.settings.dynamic_site.base.SecretManager')
    secret_manager.return_value.__enter__.return_value = DYNAMIC_SITE_BASE_SECRETS
    production = import_module('tests.dynamic_site.settings.production')
    assert production.SECRET_KEY == COMMON_PRODUCTION_SECRETS['django-logikal-secret-key']
    assert production.DATABASES['default']['HOST'] == DATABASE_SECRETS['hostname']
    assert cloud_logging_client.called
