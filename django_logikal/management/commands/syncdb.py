"""
Synchronize the local database.

Clear the public schema, apply migrations and insert local application data.

.. note:: Requires :ref:`pytest-logikal[django] <pytest-logikal:index:django>` to be installed.
.. note:: Local data must be specified in the ``local_data`` submodule of a given application in
    classes inheriting from :class:`~django_logikal.local_data.LocalData`.

.. autoclass:: django_logikal.local_data.LocalData
    :undoc-members:

.. autoclass:: django_logikal.local_data.SkipInsert
    :no-inherited-members:

.. tip:: We recommend using :doc:`factory_boy <factory-boy:index>`'s
    :class:`~factory.django.DjangoModelFactory` for generating synthetic data. By registering the
    factories in your tests (via `pytest-factoryboy
    <https://pytest-factoryboy.readthedocs.io/en/stable/>`_) you can use the same synthetic data
    for local development and testing.

"""
import inspect
from importlib import import_module
from importlib.util import find_spec
from typing import Any

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connections
from factory import random as factory_random
from logikal_utils.project import tool_config
from logikal_utils.random import DEFAULT_RANDOM_SEED

from django_logikal.local_data import LocalData, SkipInsert

DEFAULT_ALLOWED_HOSTS = ('127.0.0.1', 'localhost', 'postgres')


class Command(BaseCommand):
    help = ' '.join(__doc__.splitlines()[0:4])

    def __init__(self, *args: Any, **kwargs: Any):
        self._connection = kwargs.pop('connection', connections['default'])
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--no-input', action='store_true', help='Do not prompt for input.')

    def _clear_public_schema(self, no_input: bool) -> None:
        if not no_input:
            warning = '\nThis will DELETE ALL CURRENT DATA in the public schema!'
            self.stdout.write(self.style.WARNING(warning))
            self.stdout.write('\nAre you sure you want to do this?')
            if input('Type \'yes\' to continue, or \'no\' to cancel: ') != 'yes':
                raise CommandError('Cancelled')

        self.stdout.write(self.style.MIGRATE_HEADING('\nClearing public schema:'))
        with self._connection.cursor() as cursor:
            self.stdout.write('  Dropping schema...', ending='')
            cursor.execute('DROP SCHEMA public CASCADE')
            self.stdout.write(self.style.SUCCESS(' OK'))
            self.stdout.write('  Creating schema...', ending='')
            cursor.execute('CREATE SCHEMA public')
            self.stdout.write(self.style.SUCCESS(' OK'))

    def _run_migrations(self, options: Any) -> None:
        self.stdout.write('')
        call_command('migrate', **options)

    def _insert_local_data(self) -> None:
        # Setting seed for deterministic data
        factory_random.reseed_random(DEFAULT_RANDOM_SEED)
        info_message_shown = False
        for app in apps.get_app_configs():
            if not (module := getattr(app, 'module', None)):
                continue  # pragma: no cover, defensive line

            local_data_module_path = f'{module.__name__}.local_data'
            if not find_spec(local_data_module_path):
                continue

            if not info_message_shown:
                self.stdout.write(self.style.MIGRATE_HEADING('\nInserting local data:'))
                info_message_shown = True

            self.stdout.write(f'  Importing {local_data_module_path}... ', ending='')
            self.stdout.flush()
            local_data_module = import_module(local_data_module_path)
            self.stdout.write(self.style.SUCCESS('OK'))

            for _, local_data in inspect.getmembers(local_data_module):
                if (
                    inspect.isclass(local_data)
                    and not inspect.isabstract(local_data)
                    and issubclass(local_data, LocalData)
                ):
                    class_path = f'{local_data.__module__}.{local_data.__qualname__}'
                    self.stdout.write(f'    Inserting {class_path}... ', ending='')
                    self.stdout.flush()
                    try:
                        local_data.insert()
                        self.stdout.write(self.style.SUCCESS('OK'))
                    except SkipInsert as skip:
                        reason = str(skip)
                        reason = f' – {reason}' if reason else ''
                        self.stdout.write(self.style.WARNING('SKIPPED') + reason)

    def handle(self, *_args: Any, **options: Any) -> None:
        database = self._connection.settings_dict
        config = tool_config('django_logikal').get('syncdb', {})
        if database['HOST'] not in config.get('allowed_hosts', DEFAULT_ALLOWED_HOSTS):
            raise CommandError(f'Disallowed database host "{database['HOST']}"')

        database_url = f'{database['HOST']}:{database['PORT']}/{database['NAME']}'
        self.stdout.write(f'Synchronizing database {self.style.ERROR(database_url)}')

        self._clear_public_schema(no_input=bool(options.get('no_input')))
        self._run_migrations(options)
        self._insert_local_data()

        self.stdout.write(self.style.SUCCESS('\nDatabase successfully synchronized'))
