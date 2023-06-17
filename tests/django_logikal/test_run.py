from pytest_mock import MockerFixture

from django_logikal.run import main


def test_main(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.env.environ')  # to avoid modifying it
    mocker.patch('django_logikal.run.environ')  # to avoid modifying it
    execute = mocker.patch('django_logikal.run.execute_from_command_line')
    assert not main(['--debug', '--toolbar', '--cloud-logging', '--send-emails'])
    assert execute.called_with(['manage', 'runserver'])
