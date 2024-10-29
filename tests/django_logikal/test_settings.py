from pytest import CaptureFixture, MonkeyPatch

from django_logikal.settings import Settings, SettingsUpdate


def test_debug_messages(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    monkeypatch.setenv('DJANGO_LOGIKAL_LOG_LEVEL', 'DEBUG')
    settings = Settings({'DATABASES': []})
    settings.update(SettingsUpdate)
    assert 'DATABASES' in settings

    stdout = capsys.readouterr().out
    assert 'Settings update' in stdout
    assert 'Applying django_logikal.settings.SettingsUpdate' in stdout
