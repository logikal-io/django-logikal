from pytest import CaptureFixture
from pytest_mock import MockerFixture

from django_logikal.run import main


def test_main(mocker: MockerFixture, capsys: CaptureFixture[str]) -> None:
    mocker.patch('django_logikal.env.environ')  # to avoid modifying it
    mocker.patch('django_logikal.run.environ')  # to avoid modifying it
    execute = mocker.patch('django_logikal.run.execute_from_command_line')
    assert not main(['--debug', '--toolbar', '--offline', '--cloud-logging', '--send-emails'])
    execute.assert_called_with(['manage', 'runserver', '127.0.0.1:8000'])

    assert not main(['--help'])
    assert 'usage:' in capsys.readouterr().out
