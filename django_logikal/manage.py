"""
Execute a Django management command.
"""
import sys
from os import environ
from typing import Sequence

from django.core.management import execute_from_command_line

from django_logikal.pyproject import DJANGO_LOGIKAL_CONFIG


def main(args: Sequence[str] = tuple(sys.argv[1:])) -> int:
    sys.path.insert(0, '.')
    environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_LOGIKAL_CONFIG['DJANGO_SETTINGS_MODULE'])
    execute_from_command_line(['manage'] + list(args))
    return 0
