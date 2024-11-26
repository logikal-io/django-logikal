"""
Start the Django development web server.
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
    parser.add_argument('-t', '--toolbar', action='store_true', help='enable the debug toolbar')
    parser.add_argument('-o', '--offline', action='store_true', help='run in offline mode')
    parser.add_argument('--cloud-logging', action='store_true', help='use cloud logging')
    parser.add_argument('--send-emails', action='store_true', help='send out emails')
    util_args, manage_args = parser.parse_known_args(args)
    if util_args.debug:
        set_option('log_level', 'DEBUG')
    if util_args.toolbar:
        set_option('toolbar')
    if util_args.offline:
        set_option('offline')
    if util_args.cloud_logging:
        set_option('cloud_logging')
    if util_args.send_emails:
        set_option('send_emails')
    if '-h' in manage_args or '--help' in manage_args:
        print(f'{parser.format_help()}\nCommand:\n')

    sys.path.insert(0, '.')
    set_option('dev_run')
    environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        tool_config('django_logikal')['DJANGO_SETTINGS_MODULE'],
    )
    default_address_port = tool_config('django_logikal').get('run', {}).get('default_address_port')
    if not manage_args and default_address_port:
        manage_args.append(default_address_port)

    execute_from_command_line(['manage', 'runserver'] + manage_args)
    return 0
