from typing import List

from django.conf import global_settings
from django.core.checks import Error
from pytest_django.fixtures import SettingsWrapper

from django_logikal.apps import check_settings


def message_in_errors(message: str, errors: List[Error]) -> bool:
    return any(message in error.msg for error in errors)


def test_check_settings(settings: SettingsWrapper) -> None:
    settings.ROOT_URLCONF = None
    settings.AUTH_USER_MODEL = global_settings.AUTH_USER_MODEL
    settings.EMAIL_SUBJECT_PREFIX = global_settings.EMAIL_SUBJECT_PREFIX
    errors = check_settings()
    for index, error in enumerate(errors, start=1):
        assert error.id == f'django_logikal.E{index:03d}'
    assert message_in_errors('ROOT_URLCONF', errors)
    assert message_in_errors('AUTH_USER_MODEL', errors)
    assert message_in_errors('EMAIL_SUBJECT_PREFIX', errors)
