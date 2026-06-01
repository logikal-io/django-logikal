from pytest import raises

from django_logikal.forms.generic import Form


class InvalidForm(Form):
    """
    An invalid form class.
    """


def test_invalid_form() -> None:
    with raises(RuntimeError, match='metadata class must be specified'):
        InvalidForm()
