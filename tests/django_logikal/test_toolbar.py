from pytest import MonkeyPatch, mark
from pytest_django.fixtures import SettingsWrapper
from pytest_logikal.browser import Browser, scenarios, set_browser
from pytest_logikal.django import LiveURL
from selenium.webdriver.common.by import By

from django_logikal.settings import Settings
from django_logikal.settings.common.dev import CommonDevSettings


@mark.xfail(reason='Settings do not get applied')
@set_browser(scenarios.desktop)
def test_toolbar(
    live_app_url: LiveURL,
    browser: Browser,
    settings: SettingsWrapper,
    monkeypatch: MonkeyPatch,
) -> None:  # pragma: no cover
    # Update settings
    monkeypatch.setenv('DJANGO_LOGIKAL_TOOLBAR', '1')
    base_settings_fields = [
        'MIDDLEWARE',
        'CSP_DEFAULT_SRC',
        'INSTALLED_APPS',
        'EMAIL_BACKEND',
    ]
    changed_settings_fields = [
        'MIDDLEWARE',
        'CSP_DEFAULT_SRC',
        'INSTALLED_APPS',
        'INTERNAL_IPS',
        'DEBUG_TOOLBAR_PANELS',
        'DEBUG_TOOLBAR_CONFIG',
        'EMAIL_BACKEND',
    ]
    base_settings = {setting: getattr(settings, setting) for setting in base_settings_fields}
    dev_settings = Settings(base_settings).update(CommonDevSettings)
    for field in changed_settings_fields:
        setattr(settings, field, dev_settings[field])

    # Load page
    browser.get(live_app_url('models'))
    browser.find_element(By.ID, 'djDebugToolbarHandle').click()

    # Freeze undeterministic values
    timer_panel = browser.find_element(By.ID, 'djdt-TimerPanel')
    browser.replace_text(timer_panel.find_element(By.TAG_NAME, 'small'), "CPU: 0.00ms (0.00ms)")

    template_panel = browser.find_element(By.ID, 'djdt-TemplateProfilerPanel')
    browser.replace_text(template_panel.find_element(By.TAG_NAME, 'small'), "1 calls in 0.00 ms")

    sql_panel = browser.find_element(By.ID, 'djdt-SQLPanel')
    browser.replace_text(sql_panel.find_element(By.TAG_NAME, 'small'), '"2 queries in 0.00ms"')

    # Check toolbar
    browser.check('menu')
    browser.find_element(By.ID, 'djdt-CachePanel').click()
    browser.find_element(By.ID, 'CachePanel').find_element(By.TAG_NAME, 'h4')  # waits for loading
    browser.check('page')
