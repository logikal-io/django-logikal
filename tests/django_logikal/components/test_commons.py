from pytest_logikal import Browser, set_browser

from tests.django_logikal import scenarios
from tests.django_logikal.components import docs_url, macro_example


@set_browser(scenarios.desktop)
def test_menu(browser: Browser, theme: str) -> None:
    browser.get(docs_url('commons'))
    browser.check(theme, element=macro_example(browser, 'commons.menu', theme=theme))


@set_browser(scenarios.desktop)
def test_language_switcher(browser: Browser, theme: str) -> None:
    browser.get(docs_url('commons'))
    browser.check(theme, element=macro_example(browser, 'commons.language_switcher', theme=theme))
