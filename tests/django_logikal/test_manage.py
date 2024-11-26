from pytest import CaptureFixture
from pytest_mock import MockerFixture

from django_logikal.manage import main


def test_main(mocker: MockerFixture, capsys: CaptureFixture[str]) -> None:
    mocker.patch('django_logikal.env.environ')  # to avoid modifying it
    mocker.patch('django_logikal.manage.environ')  # to avoid modifying it
    execute = mocker.patch('django_logikal.manage.execute_from_command_line')
    assert not main(['makemigrations', '--debug', '--offline', '--cloud-logging'])
    execute.assert_called_with(['manage', 'makemigrations'])

    assert not main(['--help'])
    assert 'usage:' in capsys.readouterr().out
