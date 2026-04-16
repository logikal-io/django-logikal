from pytest_logikal import Browser, set_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.django_logikal import scenarios
from tests.django_logikal.components import docs_url, macro_example


@set_browser(scenarios.desktop)
def test_menu(browser: Browser, theme: str) -> None:
    browser.get(docs_url('commons'))
    browser.check(theme, element=macro_example(browser, 'commons.menu', theme=theme))


@set_browser(scenarios.desktop)
def test_input_field(browser: Browser, theme: str) -> None:
    browser.get(docs_url('commons'))
    example = macro_example(browser, 'commons.input_field', theme=theme)
    browser.check(theme, element=example)

    # Active state
    root = example.shadow_root
    input_field = root.find_element(By.CSS_SELECTOR, 'input')
    input_field.click()
    browser.check(f'{theme}_active', element=example)

    # Invalid state
    input_field.send_keys('invalid')
    browser.check(f'{theme}_invalid_active', element=example)
    input_field.send_keys(Keys.TAB)
    browser.check(f'{theme}_invalid_inactive', element=example)

    # Valid state
    input_field.click()
    browser.check(f'{theme}_invalid_active_again', element=example)
    input_field.clear()
    browser.check(f'{theme}_invalid_active_clear', element=example)
    input_field.send_keys('valid@example.com')
    browser.check(f'{theme}_valid', element=example)
