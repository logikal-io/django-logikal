"""
Generate static files.

.. note:: Requires the :ref:`static extra <index:Static Sites>`.
"""
from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = ' '.join(__doc__.splitlines()[0:2])

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--no-input', action='store_true', help='Do not prompt for input.')
        parser.add_argument('output_dir', nargs='?', help='The output folder to use.')

    def handle(self, *_args: Any, **options: dict[str, Any]) -> None:
        no_input = options.pop('no_input', False)
        output_dir = options.pop('output_dir', None)
        call_command('collectstatic', clear=True, no_input=not no_input, **options)
        call_command('distill-local', force=no_input, output_dir=output_dir, **options)
