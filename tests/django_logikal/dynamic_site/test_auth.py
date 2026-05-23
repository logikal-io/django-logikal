import re
from time import sleep

from anymail.message import AnymailMessage
from pytest_logikal import Browser, LiveURL, set_browser
from selenium.webdriver.common.by import By

from tests.django_logikal import scenarios
from tests.django_logikal.factories import USER_PASSWORD, UserFactory
from tests.dynamic_site.models import User

NEW_USER_PASSWORD = 'new_user_password'  # nosec: only used for testing


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
    password.send_keys(NEW_USER_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('reset_password_successful')

    # Log in with the new password
    password = browser.find_element(By.ID, 'id_password')
    password.send_keys(NEW_USER_PASSWORD)
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
    email_input.send_keys('test-user-temporary@django-logikal.org')
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
    new_password.send_keys(NEW_USER_PASSWORD)
    sleep(2)
    browser.check('change_password_valid')

    browser.find_element(By.CSS_SELECTOR, '.actions button').click()
    browser.check('after_change_password')

    # Log out and log in again with the new password
    browser.find_element(By.CSS_SELECTOR, 'form button').click()
    login(live_url=live_url, browser=browser, user=user, password=NEW_USER_PASSWORD)
    browser.check('after_login_with_new')


@set_browser(scenarios.desktop)
def test_social_auth(live_url: LiveURL, browser: Browser) -> None:
    browser.get(live_url('account_auth'))
