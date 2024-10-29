import logging
import warnings
from collections.abc import Callable
from time import localtime, strftime
from typing import Any

from django.conf import settings
from google.cloud import logging as cloud_logging
from termcolor import colored


class ConsoleLogFormatter(logging.Formatter):
    _STYLES: dict[str, Any] = {
        'timestamp': {'color': 'magenta'},
        'level': {
            'DEBUG': {'color': 'blue'},
            'INFO': {'color': 'white', 'attrs': ['dark']},
            'WARNING': {'color': 'red'},
            'ERROR': {'color': 'red', 'attrs': ['bold']},
            'CRITICAL': {'color': 'red', 'attrs': ['bold']},
        },
        'place': {'color': 'white', 'attrs': ['dark']},
        'status_code': {
            'HTTP_INFO': {'attrs': ['bold']},
            'HTTP_NOT_MODIFIED': {'color': 'cyan'},
            'HTTP_REDIRECT': {'color': 'green'},
            'HTTP_NOT_FOUND': {'color': 'yellow'},
            'HTTP_BAD_REQUEST': {'color': 'red', 'attrs': ['bold']},
            'HTTP_SERVER_ERROR': {'color': 'magenta', 'attrs': ['bold']},
        }
    }

    def colored_message(self, message: str, status_code: int | None) -> str:
        if not status_code or (200 <= status_code < 300):
            return message
        if 100 <= status_code < 200:
            style = 'HTTP_INFO'
        elif status_code == 304:
            style = 'HTTP_NOT_MODIFIED'
        elif 300 <= status_code < 400:
            style = 'HTTP_REDIRECT'
        elif status_code == 404:
            style = 'HTTP_NOT_FOUND'
        elif 400 <= status_code < 500:
            style = 'HTTP_BAD_REQUEST'
        else:
            style = 'HTTP_SERVER_ERROR'
        return colored(message, **self._STYLES['status_code'][style])

    def format(self, record: logging.LogRecord) -> str:
        timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime(record.created))
        timestamp = colored(f'{timestamp}.{record.msecs:03.0f}', **self._STYLES['timestamp'])
        level = record.levelname
        level = colored(level, **(self._STYLES['level'].get(level, self._STYLES['level']['INFO'])))
        place = f'({record.name}:{record.lineno})'
        place = colored(place, **self._STYLES['place'])
        message = record.getMessage().strip()
        message = self.colored_message(message, status_code=getattr(record, 'status_code', None))

        if exception := (getattr(record, 'exc_info', '') or ''):
            exception = '\n' + self.formatException(record.exc_info)  # type: ignore[arg-type]
        if stack := (getattr(record, 'stack_info', '') or ''):
            stack = '\n' + self.formatStack(record.stack_info)  # type: ignore[arg-type]

        return f'{timestamp} {level} {message} {place}{exception}{stack}'

    @staticmethod
    def warning_formatter() -> Callable[..., str]:
        def formatwarning(
            message: Warning, category: type[Warning], filename: str, lineno: int,
            *_args: Any, **_kwargs: Any,
        ) -> str:
            cleaned_message = str(message).replace('\n', ' ').replace('  ', ' ').strip()
            return f'{category.__name__}: {cleaned_message} ({filename}:{lineno})'
        return formatwarning


def logging_config(
    log_level: str = 'INFO',
    console: bool = True,
    cloud: bool = False,
) -> dict[str, Any]:
    config: dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {'console': {'()': ConsoleLogFormatter}},
        'handlers': {
            'console': {'class': 'logging.StreamHandler', 'formatter': 'console', 'filters': []},
        },
        'loggers': {
            'django': {'propagate': True, 'handlers': []},
            'django.db': {'propagate': True, 'handlers': [], 'level': log_level},
        },
        'root': {'level': log_level, 'handlers': []},
    }

    if console:
        config['root']['handlers'].append('console')
        warnings.formatwarning = ConsoleLogFormatter.warning_formatter()

    if cloud:
        from stormware.google.auth import GCPAuth  # pylint: disable=import-outside-toplevel

        auth = GCPAuth()
        client = cloud_logging.Client(  # type: ignore[no-untyped-call]
            project=auth.project_id(),
            credentials=auth.credentials(),
        )
        config['handlers']['cloud'] = {
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': client,
            'name': f'django-{settings.SETTINGS_MODULE.rsplit('.', 1)[-1].replace('_', '-')}',
        }
        config['root']['handlers'].append('cloud')

    return config
