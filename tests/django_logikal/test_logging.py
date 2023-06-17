import logging
import sys
from typing import Any, Optional

from django_logikal.logging import ConsoleLogFormatter


def record(
    level: int,
    status_code: Optional[int] = None,
    message: Optional[str] = None,
    exc_info: Any = None,
    stack: Optional[str] = None,
) -> logging.LogRecord:
    log_record = logging.LogRecord(
        name='test_name', level=level, pathname='test_path', lineno=1,
        msg=message or f'Status {status_code}', args={}, exc_info=exc_info, sinfo=stack,
    )
    if status_code is not None:
        log_record.status_code = status_code
    return log_record


# Note: this test needs to be observed in live mode to check colors and formatting
def test_colored_message() -> None:
    formatter = ConsoleLogFormatter()
    print('Example log entries')

    # Debug messages
    print(formatter.format(record(logging.DEBUG)))

    # Normal responses
    print(formatter.format(record(logging.INFO, 100)))
    print(formatter.format(record(logging.INFO, 200)))
    print(formatter.format(record(logging.INFO, 302)))
    print(formatter.format(record(logging.INFO, 304)))

    # Error responses
    print(formatter.format(record(logging.WARNING, 404)))
    print(formatter.format(record(logging.ERROR, 400)))
    print(formatter.format(record(logging.ERROR, 500)))

    # Exceptions
    try:
        raise RuntimeError('Test')
    except RuntimeError:
        print(formatter.format(record(
            level=logging.ERROR, status_code=500,
            message='Internal Server Error',
            exc_info=sys.exc_info(), stack='Stack Trace')
        ))

    # Warnings
    print(formatter.warning_formatter()(
        message=UserWarning('Test\nThis'), category=UserWarning,
        filename='test_file', lineno=1,
    ))
