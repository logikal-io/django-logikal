from pytest_mock import MockerFixture

from django_logikal.settings import Settings, SettingsUpdate


def test_debug_messages(mocker: MockerFixture) -> None:
    mocker.patch('django_logikal.settings.get_option', return_value='DEBUG')
    settings = Settings({'DATABASES': []})
    settings.update(SettingsUpdate)
    assert 'DATABASES' in settings
