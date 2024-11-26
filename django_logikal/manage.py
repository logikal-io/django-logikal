"""
Execute a Django management command.
"""
import argparse
import sys
from collections.abc import Sequence
from os import environ

from django.core.management import execute_from_command_line
from logikal_utils.project import tool_config

from django_logikal.env import set_option


def main(args: Sequence[str] = tuple(sys.argv[1:])) -> int:
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('-d', '--debug', action='store_true', help='use debug logging level')
    parser.add_argument('-o', '--offline', action='store_true', help='run in offline mode')
    parser.add_argument('--cloud-logging', action='store_true', help='use cloud logging')
    util_args, manage_args = parser.parse_known_args(args)
    if util_args.debug:
        set_option('log_level', 'DEBUG')
    if util_args.offline:
        set_option('offline')
    if util_args.cloud_logging:
        set_option('cloud_logging')
    if '-h' in manage_args or '--help' in manage_args:
        print(f'{parser.format_help()}\nCommand:{'' if len(manage_args) == 1 else '\n'}')

    sys.path.insert(0, '.')
    environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        tool_config('django_logikal')['DJANGO_SETTINGS_MODULE'],
    )
    execute_from_command_line(['manage'] + manage_args)
    return 0
