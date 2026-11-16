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

    # Hover "home" disabled current menu item
    browser.hover(root.find_element(By.ID, f'menu-{variant}-home'))
    browser.check(ready_state, element=example)

    # Hover "blog" menu item
    blog_menu_item = root.find_element(By.ID, f'menu-{variant}-blog')
    browser.hover(blog_menu_item)
    browser.check(f'blog_menu_hover_{theme_variant}', element=example, retain_hover=True)

    # Open "blog" menu item
    blog_menu_item.click()
    browser.check(f'blog_menu_open_{theme_variant}', element=example)

    # Close "blog" menu item
    blog_menu_item.click()
    browser.check(ready_state, element=example)

    # Open "blog" and then "info" menu item
    blog_menu_item.click()
    info_menu_item = root.find_element(By.ID, f'menu-{variant}-info')
    info_menu_item.click()
    browser.check(f'info_menu_open_{theme_variant}', element=example)

    # Hover "blog" menu item (after opening)
    browser.hover(blog_menu_item)
    browser.check(f'blog_menu_open_hover_{theme_variant}', element=example, retain_hover=True)

    # Hover "info" menu item (after opening)
    browser.hover(info_menu_item)
    browser.check(f'info_menu_open_hover_{theme_variant}', element=example, retain_hover=True)

    # Hover "info" menu "about" submenu item
    browser.hover(root.find_element(By.ID, f'menu-{variant}-about'))
    browser.check(f'about_submenu_hover_{theme_variant}', element=example, retain_hover=True)

    # Hover "info" menu "components" submenu item
    components_menu_item = root.find_element(By.ID, f'menu-{variant}-components')
    browser.hover(components_menu_item)
    browser.check(f'components_submenu_hover_{theme_variant}', element=example, retain_hover=True)

    # Open "info" menu "components" submenu item
    components_menu_item.click()
    browser.check(f'components_submenu_open_{theme_variant}', element=example)

    # Hover "info" menu "components" submenu item (after opening)
    browser.hover(components_menu_item)
    browser.check(
        f'components_submenu_open_hover_{theme_variant}',
        element=example, retain_hover=True,
    )

    # Hover "info" menu "components" submenu "buttons" item
    browser.hover(root.find_element(By.ID, f'menu-{variant}-buttons'))
    browser.check(f'buttons_subsubmenu_hover_{theme_variant}', element=example, retain_hover=True)

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

    # Hover language switcher
    language_switcher = root.find_element(By.ID, 'language-switcher')
    browser.hover(language_switcher)
    browser.check(f'hover_{theme}', element=example, retain_hover=True)

    # Open language switcher
    language_switcher.click()
    browser.check(f'open_{theme}', element=example)

    # Hover language switcher item
    browser.hover(language_switcher.find_element(By.CSS_SELECTOR, 'button[value="en-gb"]'))
    browser.check(f'hover_item_{theme}', element=example, retain_hover=True)

    # Close language switcher
    language_switcher.click()
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
