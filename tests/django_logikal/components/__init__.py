from pathlib import Path
from time import sleep

from pytest_logikal import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def docs_url(module: str) -> str:
    build_url = f'file://{Path(__file__).parents[3] / 'docs/build/components/'}'
    return f'{build_url}/{module}.html'


def load_docs(browser: Browser, module: str) -> None:
    browser.get(docs_url(module))
    browser.execute_async_script("""
        const done = arguments[arguments.length - 1];
        document.querySelector('.wy-nav-content').style.maxWidth = '1000px';
        document.querySelectorAll('.jinja-render-block').forEach((example) => {
            example.shadowRoot.querySelector('.jinja-example-content').style.zoom = '1';
        });
        window.dispatchEvent(new Event('resize'));
        window.requestAnimationFrame(() => window.requestAnimationFrame(() => done()));
    """)


def macro_example(browser: Browser, name: str, theme: str) -> WebElement:
    sleep(0.5)
    macro_id = f'jinja-macro-{name.replace('.', '-')}'
    macro_description = browser.find_element(By.CSS_SELECTOR, f'#{macro_id} + dd')
    return macro_description.find_element(By.CSS_SELECTOR, f'.jinja-render-block.theme-{theme}')


def jinja_example(browser: Browser, section: str, theme: str, index: int = 0) -> WebElement:
    sleep(0.5)
    selector = f'section#{section} .jinja-render-block.theme-{theme}'
    return browser.find_elements(By.CSS_SELECTOR, selector)[index]
