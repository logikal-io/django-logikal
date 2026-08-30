from collections.abc import Iterable

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.state import ProjectState
from django.db.models import Model
from psycopg import sql

from django_logikal.migration.operations.base import SQLOperation

TABLE_PRIVILEGES = {
    'ALL',
    'ALL PRIVILEGES',
    'DELETE',
    'INSERT',
    'MAINTAIN',
    'REFERENCES',
    'SELECT',
    'TRIGGER',
    'TRUNCATE',
    'UPDATE',
}


class ModelAccessOperation(SQLOperation):
    def __init__(
        self,
        models: Iterable[type[Model]],
        roles: Iterable[str],
        accesses: Iterable[str] = ('SELECT', ),
    ):  # noqa: D205, D400, D415
        """
        Args:
            models: An iterable of models to which the operation applies.
            roles: An iterable of roles to which the accesses apply.
            accesses: An iterable of accesses to manage.

        """
        tables: list[str] = []
        for model in models:
            tables.append(model._meta.db_table)
            if history_field := getattr(model._meta, 'simple_history_manager_attribute', None):
                history_model = getattr(model, history_field).model
                tables.append(history_model._meta.db_table)

        accesses = [access.upper() for access in accesses]
        if invalid_accesses := set(accesses) - TABLE_PRIVILEGES:
            raise ValueError(f'Invalid table privileges: {sorted(invalid_accesses)}')

        self.accesses = sql.SQL(', ').join(sql.SQL(access) for access in accesses)
        self.tables = sql.SQL(', ').join(sql.Identifier(table) for table in tables)
        self.roles = sql.SQL(', ').join(sql.Identifier(role) for role in roles)


class GrantModelAccess(ModelAccessOperation):
    """
    Grant access to a given set of models.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('GRANT {accesses} ON {tables} TO {roles}').format(
            accesses=self.accesses, tables=self.tables, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('REVOKE {accesses} ON {tables} FROM {roles}').format(
            accesses=self.accesses, tables=self.tables, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)


class RevokeModelAccess(ModelAccessOperation):
    """
    Revoke access from a given set of models.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('REVOKE {accesses} ON {tables} FROM {roles}').format(
            accesses=self.accesses, tables=self.tables, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('GRANT {accesses} ON {tables} TO {roles}').format(
            accesses=self.accesses, tables=self.tables, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)
