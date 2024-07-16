# pylint: disable=import-outside-toplevel
from django.db.migrations.writer import MigrationWriter


class FormattedMigrationWriter(MigrationWriter):
    """
    Write nicely formatted migration files.

    Uses `Black <https://black.readthedocs.io/en/stable/>`_ and `isort
    <https://pycqa.github.io/isort/>`_ with settings compatible with :ref:`pytest-logikal
    <pytest-logikal:index:Getting Started>`.

    .. note:: Requires :ref:`pytest-logikal <pytest-logikal:index:Installation>` to be installed.
    """
    def as_string(self) -> str:
        """
        Return a string of the nicely formatted file contents.
        """
        import black
        import isort
        from pytest_logikal.black import get_mode as black_mode
        from pytest_logikal.isort import get_config as isort_config
        from pytest_logikal.utils import get_ini_option

        max_line_length = get_ini_option('max_line_length')
        code = super().as_string()
        code = black.format_str(code, mode=black_mode(max_line_length))
        return isort.api.sort_code_string(code, **isort_config(max_line_length=max_line_length))
