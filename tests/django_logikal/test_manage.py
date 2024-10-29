from pytest_mock import MockerFixture

from django_logikal.manage import main


def test_main(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.manage.environ')  # to avoid modifying it
    execute = mocker.patch('django_logikal.manage.execute_from_command_line')
    args = ['makemigrations']
    assert not main(args=args)
    execute.assert_called_with(['manage'] + args)
