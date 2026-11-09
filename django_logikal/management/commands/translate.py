"""
Manage translation message catalogs.
"""
import logging
import os
import sys
from collections.abc import Iterator, Sequence
from datetime import datetime
from importlib import metadata
from pathlib import Path
from typing import Any, cast

import django
from babel.messages.frontend import CommandLineInterface
from babel.messages.pofile import read_po
from django.core.management.base import BaseCommand, CommandError, CommandParser
from logikal_utils.project import project_name, tool_config

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

    @staticmethod
    def _project_name() -> str:
        return str(
            tool_config('django_logikal').get('translate', {}).get('project')
            or project_name(raise_error_on_missing=True)
        )

    def _remove_empty_template(self, app: App, domain: str, output: Path | None) -> None:
        template = (output or app.path) / f'locale/{domain}.pot'
        with template.open('rb') as template_file:
            empty = not read_po(template_file)
        if empty:
            self.stdout.write(f'removing empty PO template file {template}')
            template.unlink()

    def _po_filename(self, domain: str, locale: str) -> str:
        suffix = {'django': '', 'djangojs': 'js'}[domain]
        suffix = f'_{suffix}' if suffix else ''
        return f'{self._project_name().replace('-', '_')}_{locale.lower()}{suffix}.po'

    def _po_files(self, app: App, domain: str, output: Path | None) -> Iterator[tuple[Path, str]]:
        translations_path = (output or app.path) / 'translations'
        for path in translations_path.glob(self._po_filename(domain=domain, locale='*')):
            with path.open('rb') as file:
                catalog = read_po(file)
            if catalog.locale is None:
                raise CommandError(f'Missing "Language" header in "{path}"')
            locale = str(catalog.locale)
            if path.name == self._po_filename(domain=domain, locale=locale):
                yield path, locale

    def _extract(self, app: App, output: Path | None, update: bool = False) -> None:
        locale_path = (output or app.path) / 'locale'
        locale_path.mkdir(parents=True, exist_ok=True)
        for domain in DOMAINS:
            mapping_file = Path(__file__).parents[2] / f'babel/{domain}.toml'
            self.stdout.write(
                self.style.MIGRATE_HEADING('\nUpdating PO template file for ')
                + self.style.WARNING(domain)
                + self.style.MIGRATE_HEADING(':')
            )
            args = [
                sys.argv[0], 'extract',
                # Configuration
                '--mapping-file', str(mapping_file),
                '--width', DEFAULT_WIDTH,
                '--sort-by-file',
                '--add-location', 'file',
                '--add-comments', 'Translators:',
                # Metadata
                '--project', self._project_name(),
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
                package = project_name(raise_error_on_missing=True)
                version = metadata.version(package)  # type: ignore[arg-type]
                args.extend(['--version', f'v{version}'])
            except (metadata.PackageNotFoundError, RuntimeError):  # pragma: no cover
                pass  # pragma: no cover, ignore missing version data
            CommandLineInterface().run(args)  # type: ignore[no-untyped-call]
            if not update or not any(self._po_files(app=app, domain=domain, output=output)):
                self._remove_empty_template(app=app, domain=domain, output=output)
        self.stdout.write()

    def action_init(self, apps: Sequence[App], locale: str, output: Path | None) -> None:
        app_names = ', '.join(self.style.ERROR(app.name) for app in apps)
        self.stdout.write(f'Creating message catalogs for {app_names}\n')

        # Checking for overwrites
        output_files = {
            app.name: {
                domain: (
                    (output or app.path) / 'translations'
                    / self._po_filename(domain=domain, locale=locale)
                )
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
                if not ((output or app.path) / f'locale/{domain}.pot').exists():
                    continue
                output_file = output_files[app.name][domain]
                output_file.parent.mkdir(parents=True, exist_ok=True)
                CommandLineInterface().run([  # type: ignore[no-untyped-call]
                    sys.argv[0], 'init',
                    '--domain', domain,
                    '--input-file', str((output or app.path) / f'locale/{domain}.pot'),
                    '--output-file', str(output_file),
                    '--locale', locale,
                    '--width', DEFAULT_WIDTH,
                ])

        self.stdout.write(self.style.SUCCESS('\nMessage catalog successfully created'))

    def action_update(self, apps: Sequence[App], output: Path | None) -> None:
        for index, app in enumerate(apps):
            prefix = '\n' if index > 0 else ''
            self.stdout.write(f'{prefix}Updating catalogs for {self.style.ERROR(app.name)}')
            self._extract(app=app, output=output, update=True)
            self.stdout.write(self.style.MIGRATE_HEADING(f'{prefix}Updating catalog files:'))
            for domain in DOMAINS:
                template = (output or app.path) / f'locale/{domain}.pot'
                for catalog, locale in self._po_files(app=app, domain=domain, output=output):
                    CommandLineInterface().run([  # type: ignore[no-untyped-call]
                        sys.argv[0], 'update',
                        '--domain', domain,
                        '--locale', locale,
                        '--input-file', str(template),
                        '--output-file', str(catalog),
                        '--width', DEFAULT_WIDTH,
                        '--update-header-comment',
                    ])
                if template.exists():
                    self._remove_empty_template(app=app, domain=domain, output=output)
            self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Message catalogs successfully updated'))

    def action_compile(self, apps: Sequence[App], output: Path | None) -> None:
        for app in apps:
            self.stdout.write(f'Compiling message catalogs for {self.style.ERROR(app.name)}\n\n')
            locale_path = (output or app.path) / 'locale'
            for domain in DOMAINS:
                for catalog, locale in self._po_files(app=app, domain=domain, output=output):
                    messages_path = locale_path / locale / 'LC_MESSAGES'
                    messages_path.mkdir(parents=True, exist_ok=True)
                    CommandLineInterface().run([  # type: ignore[no-untyped-call]
                        sys.argv[0], 'compile',
                        '--domain', domain,
                        '--locale', locale,
                        '--input-file', str(catalog),
                        '--output-file', str(messages_path / f'{domain}.mo'),
                        '--statistics',
                    ])
            self.stdout.write()
        self.stdout.write(self.style.SUCCESS('Message catalogs successfully compiled'))
