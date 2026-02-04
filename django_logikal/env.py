from os import environ, getenv

PREFIX = 'DJANGO_LOGIKAL_'


def get_option(option: str, default: str = '') -> str:
    """
    Get the value of a given environment option.
    """
    return getenv(f'{PREFIX}{option.upper()}', default=default)


def set_option(option: str, value: str = '1') -> None:
    """
    Set a given environment option to the provided value.
    """
    environ[f'{PREFIX}{option.upper()}'] = value


def option_is_set(option: str) -> bool:
    """
    Check if the given option has been set.
    """
    return get_option(option) == '1'


def is_dev_env() -> bool:
    """
    Check whether the environment is a local development environment.
    """
    return option_is_set('dev_run')


def is_testing_env() -> bool:
    """
    Check whether the environment is a testing environment.
    """
    return option_is_set('testing')
