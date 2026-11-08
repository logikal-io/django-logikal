from pytest import mark
from pytest_logikal import Browser, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.django_logikal.components import jinja_example, load_docs, macro_example


@set_browser(scenarios.desktop)
def test_navigation(browser: Browser, theme: str) -> None:
    load_docs(browser, 'commons')
    browser.check(theme, element=jinja_example(browser, 'navigation', theme=theme))


@set_browser(scenarios.desktop)
def test_buttons(browser: Browser, theme: str) -> None:
    load_docs(browser, 'commons')
    for section in ['text-buttons', 'icon-buttons', 'icon-link-buttons']:
        name = f'{section.replace('-', '_')}_{theme}'
        browser.check(name, element=jinja_example(browser, section, theme=theme))


@set_browser(scenarios.desktop)
def test_popover(browser: Browser, theme: str) -> None:
    load_docs(browser, 'commons')
    browser.check(theme, element=jinja_example(browser, 'popover', theme=theme))


@mark.parametrize('variant', ['desktop', 'mobile'])
@set_browser(scenarios.desktop)
def test_menu(browser: Browser, theme: str, variant: str) -> None:
    load_docs(browser, 'commons')
    example = macro_example(browser, f'commons.{variant}_menu', theme=theme)
    root = example.shadow_root
    theme_variant = f'{theme}_{variant}'
    browser.check(theme_variant, element=example)

    if variant == 'mobile':
        # Open mobile menu
        menu_toggle = root.find_element(By.ID, 'menu-mobile-toggle')
        menu_toggle.click()
        ready_state = f'menu_open_{theme_variant}'
        browser.check(ready_state, element=example)

        # Close mobile menu
        menu_toggle.click()
        browser.check(theme_variant, element=example)

        # Open mobile menu again
        menu_toggle.click()
        browser.check(ready_state, element=example)
    else:
        ready_state = theme_variant

    # Open "blog" menu item
    root.find_element(By.ID, f'menu-blog-{variant}').click()
    browser.check(f'blog_menu_open_{theme_variant}', element=example)

    # Close "blog" menu item
    root.find_element(By.ID, f'menu-blog-{variant}').click()
    browser.check(ready_state, element=example)

    # Open "blog" and then "info" menu item
    root.find_element(By.ID, f'menu-blog-{variant}').click()
    root.find_element(By.ID, f'menu-info-{variant}').click()
    browser.check(f'info_menu_open_{theme_variant}', element=example)

    # Open "info" menu "components" submenu item
    root.find_element(By.ID, f'menu-components-{variant}').click()
    browser.check(f'info_submenu_open_{theme_variant}', element=example)

    # Close all items
    if variant == 'desktop':
        root.find_element(By.CSS_SELECTOR, 'nav').click()
        browser.check(ready_state, element=example)


@set_browser(scenarios.desktop)
def test_language_switcher(browser: Browser, theme: str) -> None:
    load_docs(browser, 'commons')
    example = macro_example(browser, 'commons.language_switcher', theme=theme)
    root = example.shadow_root
    browser.check(theme, element=example)

    # Open switcher
    root.find_element(By.ID, 'language-switcher').click()
    browser.check(f'open_{theme}', element=example)

    # Close switcher
    root.find_element(By.ID, 'language-switcher').click()
    browser.check(theme, element=example)


@set_browser(scenarios.desktop)
def test_messages(browser: Browser, theme: str) -> None:
    load_docs(browser, 'commons')
    example = macro_example(browser, 'commons.messages', theme=theme)
    root = example.shadow_root
    browser.check(theme, element=example)

    # Dismiss
    root.find_element(By.ID, 'messages-dismiss').click()
    browser.check(f'dismiss_{theme}', element=example)
