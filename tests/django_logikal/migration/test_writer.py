from pathlib import Path

from django_logikal.migration.writer import FormattedMigrationWriter
from tests.django_logikal.migration.create_model import Migration


def test_formatted_migration_writer() -> None:
    expected = (Path(__file__).parent / 'create_model.py').read_text()
    migration = FormattedMigrationWriter(migration=Migration('test', 'test_app')).as_string()
    assert '\n'.join(migration.splitlines()[2:]) == expected.strip()
