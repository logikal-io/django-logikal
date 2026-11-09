from pytest_logikal import Browser, set_browser

from tests.django_logikal import scenarios
from tests.django_logikal.components import jinja_example, load_docs, macro_example


@set_browser(scenarios.desktop)
def test_paragraph(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=macro_example(browser, 'text.paragraph', theme='light'))


@set_browser(scenarios.desktop)
def test_short_form_text(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=jinja_example(browser, 'short-form-text', theme='light'))


@set_browser(scenarios.desktop)
def test_long_form_text(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=jinja_example(browser, 'long-form-text', theme='light'))


@set_browser(scenarios.desktop)
def test_code_block(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=jinja_example(browser, 'code-block', theme='light'))


@set_browser(scenarios.desktop)
def test_block_quote(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=jinja_example(browser, 'block-quote', theme='light'))


@set_browser(scenarios.desktop)
def test_table(browser: Browser) -> None:
    load_docs(browser, 'text')
    browser.check(element=jinja_example(browser, 'table', theme='light'))
