import re

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe
from django.utils.text import slugify as django_slugify

SLUGIFY_TRANSLATION = str.maketrans({
    '&': 'and',
    'ø': 'o',
    'æ': 'ae',
})


def upper_first(text: str) -> str:
    """
    Change the first letter of a string to uppercase.
    """
    return text[:1].upper() + text[1:]


def join_lines(text: str, spacer: bool = False) -> str:
    """
    Replace new lines with spaces.

    Args:
        text: The text to use.
        spacer: Whether to add a space to the beginning when the text is not empty.

    """
    joined = re.sub(' +', ' ', text.replace('\n', ' ')).strip()
    prefix = ' ' if joined and spacer else ''
    return f'{prefix}{joined}'


def slugify(text: str, use_underscore: bool = False) -> str:
    """
    Convert a string to a URL slug.
    """
    slugified = django_slugify(text.translate(SLUGIFY_TRANSLATION))
    return slugified if not use_underscore else slugified.replace('-', '_')


def unslugify(text: str) -> str:
    """
    Convert a URL slug to a string.
    """
    return text.replace('and', '&').replace('-', ' ')


def wrap(text: str) -> SafeString:
    """
    Replace spaces with line breaks.
    """
    text = escape(text).replace(' &amp; ', '&nbsp;&amp;&nbsp;').replace(' ', '<br>')
    return mark_safe(text)  # nosec: text is escaped


def nowrap(text: str) -> SafeString:
    """
    Replace spaces with non-breaking spaces.
    """
    return mark_safe(escape(text).replace(' ', '&nbsp;'))  # nosec: text is escaped
