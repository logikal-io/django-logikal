from pytest_logikal import Browser, LiveURL, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios


@set_browser(scenarios.desktop)
def test_toolbar(live_app_url_with_toolbar: LiveURL, browser: Browser) -> None:
    # Load page
    browser.get(live_app_url_with_toolbar('models'))
    browser.check('handle')
    browser.find_element(By.ID, 'djDebugToolbarHandle').click()

    # Freeze undeterministic values
    timer_panel = browser.find_element(By.ID, 'djdt-TimerPanel')
    browser.replace_text(timer_panel.find_element(By.TAG_NAME, 'small'), 'CPU: 0.00ms (0.00ms)')

    template_panel = browser.find_element(By.ID, 'djdt-TemplateProfilerPanel')
    browser.replace_text(template_panel.find_element(By.TAG_NAME, 'small'), '1 calls in 0.00 ms')

    sql_panel = browser.find_element(By.ID, 'djdt-SQLPanel')
    browser.replace_text(sql_panel.find_element(By.TAG_NAME, 'small'), '1 query in 0.00ms')

    # Check toolbar
    browser.check('menu')
    browser.find_element(By.ID, 'djdt-CachePanel').click()
    browser.find_element(By.ID, 'CachePanel').find_element(By.TAG_NAME, 'h4')  # waits for loading
    browser.check('page')
