import json
import re
from time import sleep, time

import jwt
from anymail.message import AnymailMessage
from django.conf import settings
from pytest import mark
from pytest_logikal import Browser, LiveURL, set_browser
from pytest_mock import MockerFixture
from requests_mock import Mocker as RequestsMocker
from selenium.webdriver.common.by import By

from tests.django_logikal import factories, scenarios
from tests.django_logikal.factories import USER_PASSWORD, UserFactory
from tests.dynamic_site.models import User

TEST_USER = 'test-user-temporary@django-logikal.org'
TEST_USER_NEW_PASSWORD = 'test_user_new_password'  # nosec: only used for testing

SOCIAL_AUTH_SECRETS = {
    'stormware-google-oauth-client-secrets': json.dumps({
        'client_id': 'client-id',
        'client_secret': 'client-secret',  # nosec: only used for testing
    }),
}


def login(live_url: LiveURL, browser: Browser, user: User, password: str) -> None:
    browser.get(live_url('account_auth'))
    email_input = browser.find_element(By.ID, 'id_email')
    email_input.send_keys(user.email)
    browser.find_element(By.ID, 'id_form_auth').find_element(By.TAG_NAME, 'button').click()
    password_input = browser.find_element(By.ID, 'id_password')
    password_input.send_keys(password)
    browser.find_element(By.CSS_SELECTOR, '#id_form_login .actions button').click()


def reset_password(browser: Browser, user: User, mailoutbox: list[AnymailMessage]) -> None:
    # Go to "Forgot your password?"
    email_input = browser.find_element(By.ID, 'id_email')
    email_input.send_keys(user.email)
    browser.find_element(By.ID, 'id_form_auth').find_element(By.TAG_NAME, 'button').click()
    browser.find_element(By.CSS_SELECTOR, '.helptext a').click()
    browser.check('reset_password')

    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('reset_password_email')

    # Get password reset link
    email = mailoutbox[1].body
    link = re.search(r'(http://localhost:[^\n]+)', email).group(0)  # type: ignore[union-attr]
    browser.get(link)
    browser.check('reset_password_email_link')

    # Set new password
    password = browser.find_element(By.ID, 'id_password1')
    password.send_keys(TEST_USER_NEW_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('reset_password_successful')

    # Log in with the new password
    password = browser.find_element(By.ID, 'id_password')
    password.send_keys(TEST_USER_NEW_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, '.actions button').click()


@set_browser(scenarios.desktop)
def test_field_validation(live_url: LiveURL, browser: Browser) -> None:
    # See https://github.com/pytest-dev/pytest-factoryboy/issues/269
    user: User = UserFactory()  # type: ignore[assignment]

    # Load auth page
    browser.get(live_url('account_auth'))
    browser.check('auth')

    # Click on the email field
    email = browser.find_element(By.ID, 'id_email')
    email.click()
    browser.check('auth_focus')

    # Start typing the email
    user_email = user.email.split('@')
    email.send_keys(user_email[0])
    sleep(0.5)
    browser.check('auth_invalid_email')

    # Finish typing the email
    email.send_keys(f'@{user_email[1]}')
    sleep(0.5)
    browser.check('auth_valid_email')

    # Click "Next" button
    browser.find_element(By.ID, 'id_form_auth').find_element(By.TAG_NAME, 'button').click()
    browser.check('login')

    # Start typing the password
    password = browser.find_element(By.ID, 'id_password')
    password.send_keys(USER_PASSWORD[:5])
    sleep(0.5)
    browser.check('login_invalid_password')

    show_password_toggle = browser.find_element(By.CSS_SELECTOR, '.password-input .icon-toggle')
    show_password_toggle.click()
    browser.check('login_invalid_password_show')

    show_password_toggle.click()
    browser.check('login_invalid_password_hide')

    # Finish typing the password
    password.send_keys(USER_PASSWORD[5:] + '-invalid')
    sleep(0.5)
    browser.check('login_valid_password')

    # Login error message
    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('login_error')


@set_browser(scenarios.desktop)
def test_login(live_url: LiveURL, browser: Browser, mailoutbox: list[AnymailMessage]) -> None:
    user: User = UserFactory()  # type: ignore[assignment]

    # Go through the login flow
    login(live_url=live_url, browser=browser, user=user, password=USER_PASSWORD)
    browser.check('email_verification')

    # Click on email verification link
    email = mailoutbox[0].body
    link = re.search(r'(http://localhost:[^\n]+)', email).group(0)  # type: ignore[union-attr]
    browser.get(link)
    browser.check('email_verification_successful')

    # Dismiss info message
    browser.find_element(By.CSS_SELECTOR, 'dialog button').click()
    browser.check('after_login')

    # Log out
    browser.find_element(By.CSS_SELECTOR, 'form button').click()
    browser.check('after_logout')

    # Go through the reset password flow
    reset_password(browser=browser, user=user, mailoutbox=mailoutbox)
    browser.check('after_login_with_new')


@set_browser(scenarios.desktop)
def test_signup(live_url: LiveURL, browser: Browser, mailoutbox: list[AnymailMessage]) -> None:
    browser.get(live_url('account_auth'))
    email_input = browser.find_element(By.ID, 'id_email')
    email_input.send_keys(TEST_USER)
    browser.find_element(By.ID, 'id_form_auth').find_element(By.TAG_NAME, 'button').click()
    browser.get(live_url('account_signup'))

    password_input = browser.find_element(By.ID, 'id_password1')
    password_input.send_keys(USER_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('email_verification')

    email = mailoutbox[0].body
    link = re.search(r'(http://localhost:[^\n]+)', email).group(0)  # type: ignore[union-attr]
    browser.get(link)
    browser.check('email_verification_successful')


@set_browser(scenarios.desktop)
def test_password_change(live_url: LiveURL, browser: Browser) -> None:
    user: User = UserFactory()  # type: ignore[assignment]

    # Change the password
    browser.get(live_url('account_auth'))
    browser.login(user)
    browser.get(live_url('account'))
    browser.check('account')

    browser.find_element(By.CSS_SELECTOR, 'p a.button').click()
    browser.check('change_password')

    old_password = browser.find_element(By.ID, 'id_oldpassword')
    old_password.send_keys(f'{USER_PASSWORD}-invalid')
    sleep(2)
    browser.check('change_password_invalid')

    old_password.clear()
    old_password.send_keys(USER_PASSWORD)
    new_password = browser.find_element(By.ID, 'id_password1')
    new_password.send_keys(TEST_USER_NEW_PASSWORD)
    sleep(2)
    browser.check('change_password_valid')

    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('after_change_password')

    # Log out and log in again with the new password
    browser.find_element(By.CSS_SELECTOR, 'form button').click()
    login(live_url=live_url, browser=browser, user=user, password=TEST_USER_NEW_PASSWORD)
    browser.check('after_login_with_new')


def social_login(  # pylint: disable=too-many-arguments
    *,
    mocker: MockerFixture,
    requests_mock: RequestsMocker,
    live_url: LiveURL,
    browser: Browser,
    first_name: str,
    last_name: str | None = None,
) -> None:
    factories.site_factory()

    mocker.patch('stormware.google.auth.GCPAuth')
    secret_manager = mocker.patch('django_logikal.settings.common.production.SecretManager')
    secret_manager.return_value.__enter__.return_value = SOCIAL_AUTH_SECRETS

    # Generate a valid ID token
    providers = settings.SOCIALACCOUNT_PROVIDERS  # type: ignore[misc]
    client_id = providers['google']['APPS'][0]['client_id']
    payload = {
        'iss': 'https://accounts.google.com',
        'aud': client_id,
        'exp': int(time()) + 3600,
        'sub': 'mock-google-user-id',
        'email': TEST_USER,
        'email_verified': True,
    }
    if first_name:
        payload['given_name'] = first_name
    if last_name:
        payload['family_name'] = last_name

    id_token_key = 'django-logikal-secret-key-32-bytes'  # nosec: only used for testing
    id_token = jwt.encode(payload, key=id_token_key, algorithm='HS256')

    # Bypass state check
    mocker.patch(
        'allauth.socialaccount.providers.oauth2.views.statekit.unstash_state',
        return_value={'next': live_url('account')},
    )

    # Intercept Google token request
    requests_mock.real_http = True
    requests_mock.post(
        'https://oauth2.googleapis.com/token',
        json={
            'access_token': 'mock-access-token',  # nosec: only used for testing
            'id_token': id_token,
            'expires_in': 3600,
        },
        headers={'content-type': 'application/json'},
    )

    # Trigger OAuth callback
    browser.get(live_url('google_callback') + '?code=mock_code&state=mock_state')


@mark.parametrize(
    ['first_name', 'last_name', 'expected_name'],
    [['Mock', 'User', 'Mock User'], ['Mock', None, 'Mock']],
)
@set_browser(scenarios.desktop)
def test_social_auth(  # pylint: disable=too-many-arguments
    *,
    live_url: LiveURL,
    browser: Browser,
    mocker: MockerFixture,
    requests_mock: RequestsMocker,
    first_name: str,
    last_name: str | None,
    expected_name: str,
) -> None:
    social_login(
        mocker=mocker,
        requests_mock=requests_mock,
        live_url=live_url,
        browser=browser,
        first_name=first_name,
        last_name=last_name,
    )
    user = User.objects.get(email=TEST_USER)
    assert user.name == expected_name


@set_browser(scenarios.desktop)
def test_set_password(
    live_url: LiveURL,
    browser: Browser,
    mocker: MockerFixture,
    requests_mock: RequestsMocker,
) -> None:
    # Go through the social login flow
    social_login(
        mocker=mocker,
        requests_mock=requests_mock,
        live_url=live_url,
        browser=browser,
        first_name='Test',
    )
    browser.check('after_login')

    # Set new password
    browser.find_element(By.CSS_SELECTOR, 'p a.button').click()
    browser.check('set_password')

    new_password = browser.find_element(By.ID, 'id_password1')
    new_password.send_keys(TEST_USER_NEW_PASSWORD)
    sleep(2)
    browser.check('set_password_valid')

    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('after_set_password')

    # Log out and log in again with the new password
    browser.find_element(By.CSS_SELECTOR, 'form:last-of-type button').click()
    user = User.objects.get(email=TEST_USER)
    login(live_url=live_url, browser=browser, user=user, password=TEST_USER_NEW_PASSWORD)
    browser.check('after_login_with_new')
