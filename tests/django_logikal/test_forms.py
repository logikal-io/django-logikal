from pytest import raises

from django_logikal.forms.allauth import LoginForm
from django_logikal.forms.generic import Form


class InvalidForm(Form):
    """
    An invalid form class.
    """


def test_invalid_form() -> None:
    with raises(RuntimeError, match='metadata class must be specified'):
        InvalidForm()


def test_password_field_without_auto_id() -> None:
    form = LoginForm(auto_id=False)
    rendered = str(form['password'].as_field_group())
    assert ' name="password"' in rendered
    assert ' id="' not in rendered
