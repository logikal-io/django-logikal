from pathlib import Path
from time import sleep

from pytest_logikal import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def docs_url(module: str) -> str:
    build_url = f'file://{Path(__file__).parents[3] / 'docs/build/components/'}'
    return f'{build_url}/{module}.html'


def macro_example(browser: Browser, name: str, theme: str) -> WebElement:
    sleep(0.5)
    macro_id = f'jinja-macro-{name.replace('.', '-')}'
    macro_description = browser.find_element(By.CSS_SELECTOR, f'#{macro_id} + dd')
    return macro_description.find_element(By.CSS_SELECTOR, f'.jinja-render-block.theme-{theme}')
