from typing import Any

from django.apps import AppConfig
from django.conf import global_settings, settings
from django.core.checks import Error, register
from django.db.migrations import writer
from django.template.loader import get_template

from django_logikal.migration.writer import FormattedMigrationWriter


class DjangoLogikalConfig(AppConfig):
    name = 'django_logikal'
    verbose_name = 'django-logikal'

    def ready(self) -> None:
        # Load bibliographies
        if bibliographies := getattr(settings, 'BIBLIOGRAPHIES', None):
            from django_logikal.bibliography import (  # pylint: disable=import-outside-toplevel
                Bibliography,
            )

            Bibliography.add_bibliographies({
                # Note: both Django and Jinja2 templates have an origin attribute, so this is fine
                name: get_template(path).origin.name  # type: ignore[attr-defined]
                for name, path in bibliographies.items()
            })

        # Format migrations
        writer.MigrationWriter = FormattedMigrationWriter  # type: ignore[misc]


@register
def check_settings(*_args: Any, **_kwargs: Any) -> list[Error]:
    errors = []

    # Check ROOT_URLCONF
    if not getattr(settings, 'ROOT_URLCONF', None):
        errors.append(Error(
            msg='The ROOT_URLCONF setting must be specified', obj=str(settings),
            id='django_logikal.E001',
        ))

    # Check AUTH_USER_MODEL
    if (
        'django.contrib.auth' in getattr(settings, 'INSTALLED_APPS', [])
        and getattr(settings, 'AUTH_USER_MODEL', None) == global_settings.AUTH_USER_MODEL
    ):
        errors.append(Error(
            msg='A custom AUTH_USER_MODEL setting must be provided', obj=str(settings),
            id='django_logikal.E002',
        ))

    # Check EMAIL_SUBJECT_PREFIX
    if (
        'anymail' in getattr(settings, 'INSTALLED_APPS', [])
        and getattr(settings, 'EMAIL_SUBJECT_PREFIX') == global_settings.EMAIL_SUBJECT_PREFIX
    ):
        errors.append(Error(
            msg='A custom EMAIL_SUBJECT_PREFIX setting must be provided', obj=str(settings),
            id='django_logikal.E003'
        ))

    return errors
