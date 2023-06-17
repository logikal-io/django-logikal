from pathlib import Path

from django_logikal.migrations import FormattedMigrationWriter
from tests.django_logikal.migrations.migration import Migration


def test_formatted_migration_writer() -> None:
    expected = (Path(__file__).parent / 'migrations/migration.py').read_text()
    migration = FormattedMigrationWriter(migration=Migration('test', 'test_app')).as_string()
    assert '\n'.join(migration.splitlines()[2:]) == expected.strip()
