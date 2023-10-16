from os import environ, getenv

PREFIX = 'DJANGO_LOGIKAL_'


def get_option(option: str, default: str = '') -> str:
    return getenv(f'{PREFIX}{option.upper()}', default=default)


def set_option(option: str, value: str = '1') -> None:
    environ[f'{PREFIX}{option.upper()}'] = value


def option_is_set(option: str) -> bool:
    return get_option(option) == '1'


def is_dev() -> bool:
    return option_is_set('dev_run') or option_is_set('testing')
