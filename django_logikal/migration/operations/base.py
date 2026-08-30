from abc import ABC

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState
from psycopg import sql


class SQLOperation(ABC, Operation):
    @staticmethod
    def execute_statement(
        schema_editor: SchemaEditor,
        statement: sql.Composable,
        params: tuple[object, ...] = (),
    ) -> None:
        if not (connection := schema_editor.connection.connection):
            raise RuntimeError('Database connection is not initialized')
        schema_editor.execute(sql=statement.as_string(connection), params=params)

    def state_forwards(self, app_label: str, state: ProjectState) -> None:
        pass
