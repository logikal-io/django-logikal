from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from psycopg import sql
from pytest import raises
from pytest_mock import MockerFixture

from django_logikal.migration.operations.base import SQLOperation


def test_execute_statement_without_connection(mocker: MockerFixture) -> None:
    schema_editor = mocker.Mock(spec=SchemaEditor)
    schema_editor.connection = mocker.Mock()
    schema_editor.connection.connection = None

    with raises(RuntimeError, match='Database connection is not initialized'):
        SQLOperation.execute_statement(schema_editor, statement=sql.SQL('SELECT 1'))
