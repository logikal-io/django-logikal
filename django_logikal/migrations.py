import black
import isort
from django.db.migrations.writer import MigrationWriter
from pytest_logikal.isort import get_config
from pytest_logikal.utils import get_ini_option


class FormattedMigrationWriter(MigrationWriter):
    def as_string(self) -> str:
        max_line_length = get_ini_option('max_line_length')
        code = super().as_string()
        code = black.format_str(code, mode=black.Mode(  # type: ignore[attr-defined]
            line_length=max_line_length,
            string_normalization=False,
            preview=True,  # breaks up long strings, can be removed with next major release
        ))
        return isort.api.sort_code_string(code, **get_config(max_line_length=max_line_length))
