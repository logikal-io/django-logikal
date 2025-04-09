from pytest import CaptureFixture, MonkeyPatch

from django_logikal.settings import Settings, SettingsUpdate


class TestSettings(SettingsUpdate):
    @classmethod
    def apply(cls, settings: Settings) -> None:
        cls.prepend(settings['list'], 'zero')
        cls.append(settings['list'], 'two')
        cls.extend(settings['list'], ['ten', 'eleven'])
        cls.insert_before(settings['list'], 'nine', before='ten')
        cls.add(settings['list'], ['twenty'])


def test_settings_update(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    monkeypatch.setenv('DJANGO_LOGIKAL_LOG_LEVEL', 'DEBUG')

    # Check operations
    settings = Settings({'list': ['one']})
    settings.update(TestSettings)
    assert 'list' in settings
    assert settings['list'] == ['zero', 'one', 'two', 'nine', 'ten', 'eleven', 'twenty']

    # Check standard output
    stdout = capsys.readouterr().out
    assert 'Settings update' in stdout
    assert 'Applying django_logikal.settings.SettingsUpdate' in stdout
