import re
from pathlib import Path

from django.core.management.base import CommandError
from pytest import raises
from pytest_mock import MockerFixture

from django_logikal.local_data import LocalData, SkipInsert
from django_logikal.management.commands import syncdb, translate


def test_syncdb(mocker: MockerFixture) -> None:
    class TestLocalData(LocalData):
        @staticmethod
        def insert() -> None:
            pass

    class TestSkippedLocalData(LocalData):
        @staticmethod
        def insert() -> None:
            raise SkipInsert('Test')

    connection = mocker.Mock(settings_dict={'HOST': '127.0.0.1', 'PORT': '5432', 'NAME': 'test'})
    cursor = mocker.Mock()
    connection.cursor.return_value.__enter__ = cursor
    connection.cursor.return_value.__exit__ = mocker.Mock()
    call_command = mocker.patch('django_logikal.management.commands.syncdb.call_command')

    insert = mocker.spy(TestLocalData, 'insert')
    skipped_insert = mocker.spy(TestSkippedLocalData, 'insert')
    mocker.patch(
        'django_logikal.management.commands.syncdb.inspect.getmembers',
        return_value=[('test', TestLocalData), ('test_skipped', TestSkippedLocalData)],
    )

    command = syncdb.Command(connection=connection)
    command.add_arguments(parser=mocker.Mock())
    command.handle(no_input=True)

    assert cursor.called
    assert call_command.called
    assert insert.called
    assert skipped_insert.called


def test_syncdb_cancelled(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.management.commands.syncdb.input', return_value='no')
    with raises(CommandError, match='Cancelled'):
        syncdb.Command().handle()


def test_syncdb_disallowed_error(mocker: MockerFixture) -> None:
    connections = mocker.patch('django_logikal.management.commands.syncdb.connections')
    connections.__getitem__.return_value.settings_dict = {'HOST': 'disallowed'}
    with raises(CommandError, match='Disallowed database'):
        syncdb.Command().handle()


def test_translate(tmp_path: Path) -> None:
    command = translate.Command()
    common_args = ['manage', 'translate', '--output', str(tmp_path)]
    locale_path = tmp_path / 'locale'

    # Init
    command.run_from_argv([*common_args, '--init', '--locale', 'en_GB'])
    pot_file = (locale_path / 'django.pot').read_text()
    assert 'Project-Id-Version: dynamic-site' in pot_file
    assert 'msgid "Localization"\nmsgstr ""' in pot_file

    # Update
    command.run_from_argv([*common_args, '--update'])
    locale_path_en_gb = locale_path / 'en_GB/LC_MESSAGES'
    po_file = (locale_path_en_gb / 'django.po').read_text()
    assert 'Project-Id-Version: dynamic-site' in po_file
    assert 'msgid "Localization"\nmsgstr ""' in po_file
    assert re.search('PO-Revision-Date: [0-9]{4}-[0-9]{2}-[0-9]{2}', po_file)

    # Compile
    command.run_from_argv([*common_args, '--compile'])
    assert (locale_path_en_gb / 'django.mo').exists()


def test_translate_missing_app(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.management.commands.translate.tool_config', return_value={})
    with raises(CommandError, match='app name must be provided'):
        translate.Command().handle()


def test_translate_missing_action() -> None:
    with raises(CommandError, match='action must be provided'):
        translate.Command().handle()


def test_translate_init_overwrite(tmp_path: Path, mocker: MockerFixture) -> None:
    command = translate.Command()

    locale_path = tmp_path / 'locale/en_GB/LC_MESSAGES'
    locale_path.mkdir(parents=True)
    (locale_path / 'django.po').touch()
    (locale_path / 'djangojs.po').touch()

    input_obj = mocker.patch('django_logikal.management.commands.translate.input')
    input_obj.return_value = 'yes'
    command.handle(init=True, locale='en_GB', output=tmp_path, app=['admin', 'dynamic_site'])
    assert 'Project-Id-Version: dynamic-site' in (locale_path / 'django.po').read_text()

    input_obj.return_value = 'no'
    with raises(CommandError, match='Cancelled'):
        command.handle(init=True, locale='en_GB', output=tmp_path)


def test_translate_init_missing_locale() -> None:
    with raises(CommandError, match='locale must be provided'):
        translate.Command().handle(init=True)
