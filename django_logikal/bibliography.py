# pylint: disable=no-value-for-parameter
from calendar import month_name
from collections.abc import Sequence
from datetime import datetime
from logging import getLogger
from typing import Any

from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe
from pybtex.database import BibliographyData, parse_file
from pybtex.richtext import Symbol, Text
from pybtex.style.formatting import BaseStyle
from pybtex.style.template import (
    field, first_of, href, join, names, optional, optional_field, tag, together,
)

logger = getLogger(__name__)


def format_url(text: str) -> Text:
    return Text(text.replace(' ', ''))


def format_month(text: str) -> Text:
    return Text(month_name[int(text)])


def format_date(text: str) -> Text:
    text_date = datetime.strptime(text, '%Y-%m-%d').strftime('%B %-d, %Y')
    return Symbol('nbsp').join(Text(text_date).split(' '))


def dash(text: Text) -> Text:
    return Text(Symbol('ndash')).join(text.split('-'))


url = href(url=field('url', apply_func=format_url, raw=True), external=True)[
    field('url', apply_func=format_url, raw=True)
]

date = first_of[
    optional_field('date', apply_func=format_date, raw=True),
    optional[together(last_tie=True)[
        field('month', apply_func=format_month, raw=True), field('year')
    ]],
    optional_field('year'),
]


class WebStyle(BaseStyle):  # type: ignore[misc]
    @staticmethod
    def separated_names(field_name: str) -> Text:
        return names(field_name, sep=', ', sep2=' and ', last_sep=' and ')

    def get_article_template(self, *args: Any, **kwargs: Any) -> Text:
        return join(sep=', ')[
            self.separated_names('author'),
            tag('em')[field('title')],
            field('journaltitle'),
            optional[
                together(last_tie=True)['Volume', field('volume')],
                optional['(', field('number'), ')'],
            ],
            optional[together(last_tie=True)['Issue', field('issue')]],
            optional_field('note'),
            date,
            optional[together(last_tie=True)['Pages', field('pages', apply_func=dash)]],
            optional[url],
        ]

    def get_book_template(self, *args: Any, **kwargs: Any) -> Text:
        return join(sep=', ')[
            self.separated_names('author'),
            tag('em')[field('title')],
            optional_field('publisher'),
            optional_field('address'),
            date,
            optional[together(last_tie=True)['ISBN', field('isbn')]],
            optional[url],
        ]

    def get_online_template(self, *args: Any, **kwargs: Any) -> Text:
        return join(sep=', ')[
            optional[self.separated_names('author')],
            optional_field('title'),
            date,
            optional_field('note'),
            url,
        ]

    def get_inproceedings_template(self, *args: Any, **kwargs: Any) -> Text:
        return join(sep=', ')[
            self.separated_names('author'),
            tag('em')[field('title')],
            field('booktitle'),
            optional_field('series'),
            optional_field('publisher'),
            optional_field('address'),
            date,
            optional[together(last_tie=True)['ISBN', field('isbn')]],
            optional[together(last_tie=True)['Pages', field('pages', apply_func=dash)]],
            optional[url],
        ]

    def get_misc_template(self, *args: Any, **kwargs: Any) -> Text:
        return join(sep=', ')[
            optional[self.separated_names('author')],
            optional[tag('em')[field('title')]],
            optional[tag('em')[field('subtitle')]],
            date,
            optional_field('note'),
            optional[url],
        ]


class Bibliography:
    data: dict[str, BibliographyData] = {}

    def __init__(self, name: str):
        """
        Render bibliography citations and references.

        Args:
            name: The name of the bibliography configuration to use.

        """
        self._name = name
        self._data = Bibliography.data[name]
        self._index = 0
        self._references: dict[str, BibliographyData] = {}

    @classmethod
    def add_bibliographies(cls, bibliographies: dict[str, str]) -> None:
        """
        Parse and store the provided bibliographies.

        Args:
            bibliographies: A name to path mapping of the bibliographies to read.

        """
        for name, path in bibliographies.items():
            if name not in cls.data:
                logger.debug(f'Loading bibliography "{path}"')
                cls.data[name] = parse_file(path, bib_format='bibtex').lower()

    def cite(self, name: str) -> SafeString:
        """
        Render a citation to the given entry and store it in the references.

        Args:
            name: The name of the entry.

        """
        if (name := escape(name).lower()) in self._references:  # pybtex is case insensitive
            raise RuntimeError(f'Reference "{name}" has already been used')
        try:
            self._references[name] = self._data.entries[name]
        except KeyError as error:
            raise RuntimeError(f'Reference "{name}" not found in "{self._name}"') from error

        self._index += 1
        return mark_safe(  # nosec: name is escaped and index is an internal integer
            f'<a href="#ref-{name}" id="cite-{name}" class="cite">'
            f'[<span>{self._index}</span>]</a>'
        )

    def references(self, classes: Sequence[str] = ('references', )) -> SafeString:
        """
        Render the stored references as an ordered, numbered list.

        Args:
            classes: The classes to add to the ordered list element.

        """
        style = WebStyle(name_style='plain')
        items = '\n'.join(
            f'<li id="ref-{name}"><a href="#cite-{name}" class="cite up">&uarr;</a>'
            f'{style.format_entry(name, entry).text.render_as('html')}</li>'
            for name, entry in self._references.items()
        )
        return mark_safe(  # nosec: name and entries are escaped
            f'<ol class="{' '.join(classes)}">\n{items}\n</ol>'
        )
