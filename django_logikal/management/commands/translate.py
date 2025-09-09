"""
Manage translation message catalogs.
"""
import logging
import os
import sys
from collections.abc import Sequence
from datetime import datetime
from importlib import metadata
from pathlib import Path
from typing import Any, cast

import django
from babel.messages.frontend import CommandLineInterface
from django.core.management.base import BaseCommand, CommandError, CommandParser
from logikal_utils.project import PYPROJECT, tool_config

TEMPLATE_HEADER = f"""
# Translation template for project "PROJECT"
# Copyright {datetime.now().year} ORGANIZATION
"""
DEFAULT_WIDTH = 96
DOMAINS = ('django', 'djangojs')
KEYWORDS = {  # See https://github.com/python-babel/babel/issues/71
    'django': [
        # See https://docs.djangoproject.com/en/5.2/ref/utils/#module-django.utils.translation
        '_',
        'gettext',
        'gettext_lazy',
        'ngettext:1,2',
        'ngettext_lazy:1,2',
        'pgettext:1c,2',
        'pgettext_lazy:1c,2',
        'npgettext:1c,2,3',
        'npgettext_lazy:1c,2,3',
    ],
}


class App:
    def __init__(self, name: str):
        self.name = name
        app_config = django.apps.apps.get_app_config(name)
        self.path = Path(os.path.relpath(app_config.path, os.getcwd()))


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        group = parser.add_argument_group(title='actions').add_mutually_exclusive_group()
        group.add_argument('-i', '--init', action='store_true',
                           help='Initialize new message catalogs.')
        group.add_argument('-u', '--update', action='store_true',
                           help='Update message catalogs.')
        group.add_argument('-c', '--compile', action='store_true',
                           help='Compile message catalogs.')
        parser.add_argument('app', nargs='*', help='The app to translate.')
        parser.add_argument('-l', '--locale', help='Locale for the new catalogs.')
        parser.add_argument('-o', '--output', type=Path, help='Output path to use.')

    def handle(self, *_args: Any, **options: Any) -> None:
        def remove_config_info(record: logging.LogRecord) -> bool:
            if record.msg.lower() == 'extracting messages from %s%s':
                record.args = (record.args[0], '')  # type: ignore[index]
            return True

        logging.getLogger().handlers = []  # to avoid double logging
        logging.getLogger('babel').addFilter(remove_config_info)

        default_apps = tool_config('django_logikal').get('translate', {}).get('apps', [])
        if not (apps := [App(app) for app in options.get('app') or default_apps]):
            raise CommandError('At least one app name must be provided')

        output = cast(Path | None, options.get('output'))  # wrong typing

        if options.get('init'):
            if not (locale := cast(str | None, options.get('locale'))):
                raise CommandError('The locale must be provided')
            return self.action_init(apps=apps, locale=locale, output=output)
        if options.get('update'):
            return self.action_update(apps=apps, output=output)
        if options.get('compile'):
            return self.action_compile(apps=apps, output=output)

        raise CommandError('An action must be provided')

    def _extract(self, app: App, output: Path | None) -> None:
        self.stdout.write()
        locale_path = (output or app.path) / 'locale'
        locale_path.mkdir(parents=True, exist_ok=True)
        for domain in DOMAINS:
            args = [
                sys.argv[0], 'extract',
                # Configuration
                '--mapping-file', str(Path(__file__).parents[2] / f'babel/{domain}.ini'),
                '--width', DEFAULT_WIDTH,
                '--sort-by-file',
                '--add-comments', 'Translators:',
                # Metadata
                '--project', app.name.replace('_', '-'),
                '--msgid-bugs-address', tool_config('django_logikal')['translate']['contact'],
                '--copyright-holder', tool_config('django_logikal')['translate']['copyright'],
                '--header-comment', TEMPLATE_HEADER,
                # Input and output file
                '--output-file', str(locale_path / f'{domain}.pot'),
                str(app.path),
            ]
            for keyword in KEYWORDS.get(domain, []):
                args.extend(['--keyword', keyword])
            try:
                version = metadata.version(PYPROJECT['project']['name'])
                args.extend(['--version', f'v{version}'])
            except metadata.PackageNotFoundError:  # pragma: no cover
                pass  # pragma: no cover; ignore missing version data
            CommandLineInterface().run(args)  # type: ignore[no-untyped-call]
        self.stdout.write()

    def action_init(self, apps: Sequence[App], locale: str, output: Path | None) -> None:
        app_names = ', '.join(self.style.ERROR(app.name) for app in apps)
        self.stdout.write(f'Creating message catalogs for {app_names}\n')

        # Checking for overwrites
        output_files = {
            app.name: {
                domain: (output or app.path) / 'locale' / locale / f'LC_MESSAGES/{domain}.po'
                for domain in DOMAINS
            }
            for app in apps
        }
        existing_files = {
            app_name: [file for file in domain_files.values() if file.exists()]
            for app_name, domain_files in output_files.items()
        }
        if any(existing_files.values()):
            warning = '\nThis will OVERWRITE the following message catalog files:'
            self.stdout.write(self.style.WARNING(warning))
            for app_name, files in existing_files.items():
                indent = 0
                if len(existing_files) > 1:
                    indent += 2
                    self.stdout.write(indent * ' ' + self.style.ERROR(app_name))
                self.stdout.write('\n'.join((indent + 2) * ' ' + str(file) for file in files))
            self.stdout.write('\nAre you sure you want to do this?')
            prompt = 'Type \'yes\' to continue, or \'no\' to cancel: '
            if input(prompt) != 'yes':
                raise CommandError('Cancelled')

        # Creating message catalog
        for app in apps:
            if len(apps) > 1:
                self.stdout.write()
                self.stdout.write(f'Creating message catalogs for {self.style.ERROR(app.name)}\n')
            self._extract(app=app, output=output)
            for domain in DOMAINS:
                CommandLineInterface().run([  # type: ignore[no-untyped-call]
                    sys.argv[0], 'init',
                    '--domain', domain,
                    '--input-file', str((output or app.path) / f'locale/{domain}.pot'),
                    '--output-file', str(output_files[app.name][domain]),
                    '--locale', locale,
                    '--width', DEFAULT_WIDTH,
                ])

        self.stdout.write(self.style.SUCCESS('\nMessage catalog successfully created'))

    def action_update(self, apps: Sequence[App], output: Path | None) -> None:
        for app in apps:
            self.stdout.write(f'Updating catalogs for {self.style.ERROR(app.name)}\n')
            self._extract(app=app, output=output)
            for domain in DOMAINS:
                CommandLineInterface().run([  # type: ignore[no-untyped-call]
                    sys.argv[0], 'update',
                    '--domain', domain,
                    '--input-file', str((output or app.path) / f'locale/{domain}.pot'),
                    '--output-dir', str((output or app.path) / 'locale'),
                    '--width', DEFAULT_WIDTH,
                    '--update-header-comment',
                ])
            self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Message catalogs successfully updated'))

    def action_compile(self, apps: Sequence[App], output: Path | None) -> None:
        for app in apps:
            self.stdout.write(f'Compiling message catalogs for {self.style.ERROR(app.name)}\n\n')
            CommandLineInterface().run([  # type: ignore[no-untyped-call]
                sys.argv[0], 'compile',
                '--domain', ' '.join(DOMAINS),
                '--directory', str((output or app.path) / 'locale'),
                '--statistics',
            ])
            self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Message catalogs successfully compiled'))
