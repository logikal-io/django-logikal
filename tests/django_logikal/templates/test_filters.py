from django_logikal.templates import filters as f


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
