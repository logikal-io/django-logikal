from django.urls import reverse
from pytest_logikal.browser import Browser, scenarios, set_browser
from selenium.webdriver.common.by import By


@set_browser(scenarios.desktop)
def test_toolbar(live_server_subprocess: str, browser: Browser) -> None:
    browser.get(live_server_subprocess + reverse('dynamic_site:models'))
    browser.find_element(By.ID, 'djDebugToolbarHandle').click()

    # Freeze undeterministic values
    timer_panel = browser.find_element(By.ID, 'djdt-TimerPanel')
    text = timer_panel.find_element(By.TAG_NAME, 'small')
    browser.execute_script('arguments[0].innerHTML = "CPU: 0.00ms (0.00ms)"', text)  # type: ignore

    template_panel = browser.find_element(By.ID, 'djdt-TemplateProfilerPanel')
    text = template_panel.find_element(By.TAG_NAME, 'small')
    browser.execute_script('arguments[0].innerHTML = "1 calls in 0.00 ms"', text)  # type: ignore

    sql_panel = browser.find_element(By.ID, 'djdt-SQLPanel')
    text = sql_panel.find_element(By.TAG_NAME, 'small')
    browser.execute_script('arguments[0].innerHTML = "2 queries in 0.00ms"', text)  # type: ignore

    # Check toolbar
    browser.check('menu')
    browser.find_element(By.ID, 'djdt-CachePanel').click()
    browser.find_element(By.ID, 'CachePanel').find_element(By.TAG_NAME, 'h4')  # waits for loading
    browser.check('page')
