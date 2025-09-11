import pytest

from django_logikal.templates import filters as f


def test_upper_first() -> None:
    assert not f.upper_first('')
    assert f.upper_first('h') == 'H'
    assert f.upper_first('he') == 'He'
    assert f.upper_first('hello') == 'Hello'
    assert f.upper_first('Hello') == 'Hello'
    assert f.upper_first('hello world') == 'Hello world'


def test_join_lines() -> None:
    assert f.join_lines('hello') == 'hello'
    assert f.join_lines('hello\nworld') == 'hello world'
    assert f.join_lines('hello\n world') == 'hello world'
    assert f.join_lines('hello\n  world') == 'hello world'


def test_slugify() -> None:
    assert f.slugify('Hello World') == 'hello-world'
    assert f.slugify('Hello World', use_underscore=True) == 'hello_world'
    assert f.slugify('árvíztűrő tükörfúrógép') == 'arvizturo-tukorfurogep'
    assert f.slugify('Høvdingens kjære squaw får') == 'hovdingens-kjaere-squaw-far'


def test_unslugify() -> None:
    assert f.unslugify('hello-world') == 'hello world'
    assert f.unslugify('this-and-that') == 'this & that'


def test_wrap() -> None:
    assert f.wrap('hello world') == 'hello<br>world'
    assert f.wrap('hello & world') == 'hello&nbsp;&amp;&nbsp;world'


def test_nowrap() -> None:
    assert f.nowrap('hello world') == 'hello&nbsp;world'


def test_truncate() -> None:
    # Appends default ellipsis when truncated
    assert f.truncate('hello world', 5) == 'hell…'
    # No truncation when text fits
    assert f.truncate('hello world', 11) == 'hello world'
    assert f.truncate('hello world', 12) == 'hello world'
    # Custom truncation marker (three dots)
    assert f.truncate('hello world', 4, '...') == 'h...'
    # Empty truncation string => pure slice
    assert f.truncate('hello world', 4, '') == 'hell'
    # Length less or equal to truncation length raises ValueError
    with pytest.raises(ValueError):
        f.truncate('hello world', 3, '...')
    # Non-positive length raises ValueError
    with pytest.raises(ValueError):
        f.truncate('hello world', 0)
