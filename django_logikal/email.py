import re
from collections.abc import Sequence
from email.mime.base import MIMEBase
from logging import getLogger
from pathlib import Path
from typing import Any

import premailer
from antimarkdown import to_markdown
from anymail.message import AnymailMessage, AnymailStatus
from django.conf import settings
from django.template.loader import get_template
from jinja2.utils import concat

logger = getLogger(__name__)


class Email:
    """
    Create an email based on a template.

    .. note:: Requires the :ref:`dynamic extra <index:Dynamic Sites>` and a valid :doc:`Anymail
        <django-anymail:index>` configuration.

    .. tip:: We recommend using the standard :ref:`dynamic site settings <settings:Dynamic Site
        Settings>` module, which configures the :doc:`Amazon SES Anymail ESP
        <django-anymail:esps/amazon_ses>` with the standard :ref:`Stormware AWS authentication
        <stormware:auth:Amazon Web Services>` process.

    Args:
        template: The template to use.
        context: The context to use for template rendering.
        prefix: The prefix to use for the subject.
            Defaults to the value of the ``EMAIL_SUBJECT_PREFIX`` setting.
            Note that a space is automatically appended to the provided value.

    Template
    ========
    .. tip:: We recommend extending the :ref:`standard email base template <templates:Email>`.

    Blocks
    ------
    .. py:data:: subject
        :noindex:

        The email's subject *(required)*.

    .. py:data:: text
        :noindex:

        The plain text version of the email *(optional)*. Defaults to the Markdown version of the
        rendered HTML content.

    Functions
    ---------
    .. py:function:: image(path: str | ~pathlib.Path) -> str
        :noindex:

        Add an inline image from a local path to the email and return the image source string.

    Methods & Properties
    ====================

    """
    def __init__(
        self,
        template: str,
        context: dict[str, Any] | None = None,
        prefix: str | None = None,
    ):
        # Loading template
        loaded_template = get_template(template)
        self._template = loaded_template.template  # type: ignore[attr-defined]
        self._template_context = self._template.new_context(context or {})

        # Creating email instance
        if (prefix := prefix if prefix is not None else settings.EMAIL_SUBJECT_PREFIX.strip()):
            prefix += ' '
        self._email = AnymailMessage(subject=f'{prefix}{self._get_block('subject')}')

        # Rendering html
        from django.contrib.sites.models import Site  # pylint: disable=import-outside-toplevel

        html = loaded_template.render({**self._template_context, 'image': self._attach_image})
        base_url = (
            'http://127.0.0.1:8000' if settings.DEBUG
            else f'https://{Site.objects.get_current().domain}'
        )
        html = premailer.transform(html, base_url=base_url, allow_network=False)
        self._email.attach_alternative(html, mimetype='text/html')

        # Rendering text
        if (text := self._get_block('text', required=False)) is None:
            text = re.sub('<script[^<]*</script>', '', html)  # remove script elements
            text = re.sub('\n +', '\n', text)  # remove indentation
            text = text.replace('<div', '<p')  # fix div start tag
            text = text.replace('</div>', '</p>')  # fix div end tag
            text = to_markdown(text) or ''
            text = re.sub(r'([=\-#])\n+', r'\1\n', text)  # fix heading
            text = re.sub(r'^\* +', r'- ', text, flags=re.MULTILINE)  # fix unordered list
            text = re.sub(r'^([0-9]+\.) +', r'\1 ', text, flags=re.MULTILINE)  # fix ordered list
            text = text.replace('\n\n\n', '\n\n')  # fix extra newlines
            text = re.sub(r'^---$', '---\n', text, flags=re.MULTILINE)  # fix horizontal rule
        self._email.body = text.strip() + '\n'

    def _get_block(self, name: str, required: bool = True) -> str | None:
        block = self._template.blocks.get(name)
        if required and not block:
            raise RuntimeError(f'The "{name}" block must be defined in the tempate')
        return concat(block(self._template_context)).strip() if block else None

    def _attach_image(self, path: str | Path, subtype: str | None = None) -> str:
        return f'cid:{self._email.attach_inline_image_file(path=path, subtype=subtype)}'

    def attach(
        self, filename: str | MIMEBase,
        content: Any | None = None,
        mimetype: str | None = None,
    ) -> None:
        """
        Create a new file attachment and add it to the message.

        See ``attach()`` in :class:`django.core.mail.EmailMessage`.
        """
        self._email.attach(filename=filename, content=content, mimetype=mimetype)

    def attach_file(self, path: str | Path, mimetype: str | None = None) -> None:
        """
        Create a new attachment using a file from the filesystem.

        See ``attach_file()`` in :class:`django.core.mail.EmailMessage`.
        """
        self._email.attach_file(path=path, mimetype=mimetype)

    def send(  # pylint: disable=too-many-arguments
        self,
        *,
        sender: str,
        to: Sequence[str],
        cc: Sequence[str] | None = None,
        bcc: Sequence[str] | None = None,
        reply_to: Sequence[str] | None = None,
    ) -> int:
        """
        Send the email.

        Args:
            sender: The sender's address.
            to: A list of recipients.
            cc: A list of carbon copy recipients.
            bcc: A list of blind carbon copy recipients.
            reply_to: A list of addresses for replies.

        """
        logger.info('Sending email')
        self._email.from_email = sender
        self._email.to = to
        self._email.cc = cc or []
        self._email.bcc = bcc or []
        self._email.reply_to = reply_to or []
        response = self._email.send()
        info = (
            f' (status: {self.status.status}, ID {self.status.message_id})'
            if self.status.message_id is not None else ''
        )
        logger.info(f'Email sent{info}')
        return response  # type: ignore[no-any-return]

    @property
    def status(self) -> AnymailStatus:
        """
        Return the status of the email.
        """
        return self._email.anymail_status
