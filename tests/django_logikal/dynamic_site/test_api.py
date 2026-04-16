import re

from django.test import Client
from pytest_logikal import Browser, LiveURL, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.dynamic_site import local_data
from tests.dynamic_site.models import User


@set_browser(scenarios.desktop)
def test_browsable_api(live_url: LiveURL, browser: Browser, user: User) -> None:
    browser.get(live_url('api-root'))
    browser.check('before_login')

    browser.login(user)
    browser.get(live_url('api-root'))

    url = browser.find_element(By.CSS_SELECTOR, 'div.response-info a span.str')
    url_text = re.sub(':[0-9]+/', '/', url.text)  # remove the non-deterministic port number
    browser.execute_script(f'arguments[0].innerHTML = "{url_text}"', url)

    browser.check('after_login')


def test_json_api(live_url: LiveURL, client: Client, user: User) -> None:
    response = client.get(live_url('api-root'))
    assert response.status_code == 403

    client.force_login(user)
    root_response = client.get(live_url('api-root')).json()
    assert root_response == {'projects': 'http://testserver/api/projects/'}

    response = client.get(root_response['projects'])
    assert response.json() == []

    local_data.ProjectData.insert()
    response = client.get(root_response['projects'])
    assert response.json()[0] == {
        'end_date': '2023-02-10',
        'name': 'Benchmark Cutting-Edge Paradigms',
        'start_date': '2023-02-01',
        'status': 'planning',
        'url': 'http://testserver/api/projects/16419f82-8b9d-4434-a465-e150bd9c66b3/',
    }
