from django_logikal.templates import tests as t


def test_startswith() -> None:
    assert t.startswith('start end', 'start')
    assert not t.startswith('start end', 'end')
