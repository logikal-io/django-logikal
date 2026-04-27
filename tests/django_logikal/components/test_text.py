from pytest_logikal import Browser, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.django_logikal.components import docs_url


@set_browser(scenarios.desktop)
def test_short_form_text(browser: Browser, theme: str) -> None:
    browser.get(docs_url('text'))
    text = browser.find_element(
        By.CSS_SELECTOR,
        f'section#short-form-text .jinja-render-block.theme-{theme}',
    )
    browser.check(theme, element=text)


@set_browser(scenarios.desktop)
def test_long_form_text(browser: Browser, theme: str) -> None:
    browser.get(docs_url('text'))
    text = browser.find_element(
        By.CSS_SELECTOR,
        f'section#long-form-text .jinja-render-block.theme-{theme}',
    )
    browser.check(theme, element=text)
