"""
Execute a Django management command.
"""
import sys
from os import environ
from typing import Sequence

from django.core.management import execute_from_command_line
from logikal_utils.project import tool_config


def main(args: Sequence[str] = tuple(sys.argv[1:])) -> int:
    sys.path.insert(0, '.')
    environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        tool_config('django_logikal')['DJANGO_SETTINGS_MODULE'],
    )
    execute_from_command_line(['manage'] + list(args))
    return 0
