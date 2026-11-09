from pytest_logikal import Browser, set_browser

from tests.django_logikal import scenarios
from tests.django_logikal.components import jinja_example, load_docs


@set_browser(scenarios.desktop)
def test_spotlight(browser: Browser) -> None:
    load_docs(browser, 'composition')
    browser.check(element=jinja_example(browser, 'spotlight', theme='light'))


@set_browser(scenarios.desktop)
def test_split(browser: Browser) -> None:
    load_docs(browser, 'composition')
    browser.check(element=jinja_example(browser, 'split', theme='light'))
    browser.check('aside', element=jinja_example(browser, 'split', theme='light', index=1))


@set_browser(scenarios.desktop)
def test_stack(browser: Browser) -> None:
    load_docs(browser, 'composition')
    browser.check(element=jinja_example(browser, 'stack', theme='light'))
    browser.check('centered', element=jinja_example(browser, 'stack', theme='light', index=1))


@set_browser(scenarios.desktop)
def test_cards(browser: Browser) -> None:
    load_docs(browser, 'composition')
    browser.check(element=jinja_example(browser, 'cards', theme='light'))
