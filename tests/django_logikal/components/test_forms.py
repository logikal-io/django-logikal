from pytest_logikal import Browser, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.django_logikal.components import jinja_example, load_docs


@set_browser(scenarios.desktop)
def test_input_fields(browser: Browser, theme: str) -> None:
    load_docs(browser, 'forms')
    browser.check(theme, element=jinja_example(browser, 'input-fields', theme=theme))


@set_browser(scenarios.desktop)
def test_password_field(browser: Browser, theme: str) -> None:
    load_docs(browser, 'forms')
    example = jinja_example(browser, 'password-field', theme=theme)
    root = example.shadow_root
    browser.check(theme, element=example)

    # Password is hidden by default
    password = root.find_element(By.ID, 'form-example-password')
    password.send_keys('test')
    browser.check(f'hidden_focused_{theme}', element=example)

    # Show password
    toggle = root.find_element(By.ID, 'form-example-password-toggle')
    toggle.click()
    browser.check(f'visible_{theme}', element=example)

    # Hide password
    toggle.click()
    browser.check(f'hidden_{theme}', element=example)


@set_browser(scenarios.desktop)
def test_errors(browser: Browser, theme: str) -> None:
    load_docs(browser, 'forms')
    browser.check(theme, element=jinja_example(browser, 'errors', theme=theme))
