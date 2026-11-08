from pytest_logikal import Browser, set_browser

from tests.django_logikal import scenarios
from tests.django_logikal.components import load_docs, macro_example


@set_browser(scenarios.desktop)
def test_auth_form(browser: Browser, theme: str) -> None:
    load_docs(browser, 'auth')
    browser.check(theme, element=macro_example(browser, 'auth.auth_form', theme=theme))
