"""
Synchronize the local database.

Clear the public schema, apply migrations and insert local application data.

.. note:: Requires :ref:`pytest-logikal[django] <pytest-logikal:index:django>` to be installed.
.. note:: Local data must be specified in the ``local_data.py`` submodule of a given application in
    classes inheriting from :class:`~django_logikal.local_data.LocalData`.

.. autoclass:: django_logikal.local_data.LocalData
    :undoc-members:

.. tip:: We recommend using :doc:`factory_boy <factory-boy:index>`'s
    :class:`~factory.django.DjangoModelFactory` for generating synthetic data. By registering the
    factories in your tests (via `pytest-factoryboy
    <https://pytest-factoryboy.readthedocs.io/en/stable/>`_) you can use the same synthetic data
    for local development and testing.

"""
from contextlib import suppress
from importlib import import_module
from typing import Any

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connections
from factory import random as factory_random

from django_logikal.local_data import LocalData


class Command(BaseCommand):
    help = ' '.join(__doc__.splitlines()[0:4])

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--no-input', action='store_true', help='Do not prompt for input.')

    def handle(self, *_args: Any, **options: Any) -> None:
        connection = connections['default']
        database = connection.settings_dict
        if database['HOST'] != '127.0.0.1':
            raise CommandError('Only the local database can be synchronized')

        database_url = f'{database["HOST"]}:{database["PORT"]}/{database["NAME"]}'
        self.stdout.write(f'Synchronizing database {self.style.ERROR(database_url)}')
        warning = '\nThis will DELETE ALL CURRENT DATA in the public schema!'
        self.stdout.write(self.style.WARNING(warning))
        self.stdout.write('\nAre you sure you want to do this?')
        prompt = 'Type \'yes\' to continue, or \'no\' to cancel: '
        if not options.get('no_input') and input(prompt) != 'yes':
            raise CommandError('Cancelled')

        # Clear schema
        self.stdout.write(self.style.MIGRATE_HEADING('\nClearing public schema:'))
        with connection.cursor() as cursor:
            self.stdout.write('  Dropping schema...', ending='')
            cursor.execute('DROP SCHEMA public CASCADE')
            self.stdout.write(self.style.SUCCESS(' OK'))
            self.stdout.write('  Creating schema...', ending='')
            cursor.execute('CREATE SCHEMA public')
            self.stdout.write(self.style.SUCCESS(' OK'))

        # Run migrations
        self.stdout.write('')
        call_command('migrate', **options)

        # Insert local data
        from pytest_logikal import django  # pylint: disable=import-outside-toplevel

        factory_random.reseed_random(django.DEFAULT_RANDOM_SEED)  # for deterministic data
        for app in apps.get_app_configs():
            with suppress(ImportError):
                if (module := getattr(app, 'module', None)):
                    import_module(f'{module.__name__}.local_data')  # register LocalData subclasses
        if LocalData.__subclasses__():
            self.stdout.write(self.style.MIGRATE_HEADING('\nInserting local data:'))
        for local_data in LocalData.__subclasses__():
            if issubclass(local_data, LocalData):
                module = local_data.__module__
                name = local_data.__name__
                self.stdout.write(f'  Inserting {module}.{name}...', ending='')
                local_data.insert()
                self.stdout.write(self.style.SUCCESS(' OK'))

        self.stdout.write(self.style.SUCCESS('\nDatabase successfully synchronized'))
