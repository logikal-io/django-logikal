from collections.abc import Iterable

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.state import ProjectState
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


class TableAccessOperation(SQLOperation):
    def __init__(
        self,
        tables: Iterable[str],
        roles: Iterable[str],
        accesses: Iterable[str] = ('SELECT', ),
    ):  # noqa: D205, D400, D415
        """
        Args:
            tables: An iterable of tables to which the operation applies.
            roles: An iterable of roles to which the accesses apply.
            accesses: An iterable of accesses to manage.

        """
        accesses = [access.upper() for access in accesses]
        if invalid_accesses := set(accesses) - TABLE_PRIVILEGES:
            raise ValueError(f'Invalid table privileges: {sorted(invalid_accesses)}')

        self.accesses = sql.SQL(', ').join(sql.SQL(access) for access in accesses)
        self.tables = sql.SQL(', ').join(sql.Identifier(table) for table in tables)
        self.roles = sql.SQL(', ').join(sql.Identifier(role) for role in roles)


class GrantTableAccess(TableAccessOperation):
    """
    Grant access to a given set of tables.
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


class RevokeTableAccess(TableAccessOperation):
    """
    Revoke access from a given schema.
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
