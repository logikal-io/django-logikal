from pytest import mark, raises

from django_logikal.email import Email


@mark.django_db
def test_invalid_template() -> None:
    with raises(RuntimeError, match='"subject" block must be defined'):
        Email('dynamic_site/email/invalid_no_subject.html.j')
