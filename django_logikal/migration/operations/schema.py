from collections.abc import Iterable

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.state import ProjectState
from psycopg import sql

from django_logikal.migration.operations.base import SQLOperation

SCHEMA_PRIVILEGES = {'ALL', 'ALL PRIVILEGES', 'CREATE', 'USAGE'}


class SchemaAccessOperation(SQLOperation):
    def __init__(
        self,
        schemas: Iterable[str],
        roles: Iterable[str],
        accesses: Iterable[str] = ('USAGE', ),
    ):  # noqa: D205, D400, D415
        """
        Args:
            schemas: An iterable of schemas to which the operation applies.
            roles: An iterable of roles to which the accesses apply.
            accesses: An iterable of accesses to manage.

        """
        accesses = [access.upper() for access in accesses]
        if invalid_accesses := set(accesses) - SCHEMA_PRIVILEGES:
            raise ValueError(f'Invalid schema privileges: {sorted(invalid_accesses)}')

        self.accesses = sql.SQL(', ').join(sql.SQL(access) for access in accesses)
        self.schemas = sql.SQL(', ').join(sql.Identifier(schema) for schema in schemas)
        self.roles = sql.SQL(', ').join(sql.Identifier(role) for role in roles)


class GrantSchemaAccess(SchemaAccessOperation):
    """
    Grant access to a given set of schemas.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('GRANT {accesses} ON SCHEMA {schemas} TO {roles}').format(
            accesses=self.accesses, schemas=self.schemas, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('REVOKE {accesses} ON SCHEMA {schemas} FROM {roles}').format(
            accesses=self.accesses, schemas=self.schemas, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)


class RevokeSchemaAccess(SchemaAccessOperation):
    """
    Revoke access from a given set of schemas.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('REVOKE {accesses} ON SCHEMA {schemas} FROM {roles}').format(
            accesses=self.accesses, schemas=self.schemas, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('GRANT {accesses} ON SCHEMA {schemas} TO {roles}').format(
            accesses=self.accesses, schemas=self.schemas, roles=self.roles,
        )
        self.execute_statement(schema_editor, statement=statement)


class SchemaOperation(SQLOperation):
    def __init__(self, name: str):  # noqa: D205, D400, D415
        """
        Args:
            name: The schema name to use.

        """
        self.name = name


class CreateSchema(SchemaOperation):
    """
    Create a schema.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('CREATE SCHEMA IF NOT EXISTS {}').format(sql.Identifier(self.name))
        self.execute_statement(schema_editor, statement=statement)

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('DROP SCHEMA {}').format(sql.Identifier(self.name))
        self.execute_statement(schema_editor, statement=statement)

    def describe(self) -> str:
        return f'Create schema {self.name}'


class DropSchema(SchemaOperation):
    """
    Drop a schema.
    """
    reversible = False

    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('DROP SCHEMA IF EXISTS {}').format(sql.Identifier(self.name))
        self.execute_statement(schema_editor, statement=statement)

    def describe(self) -> str:
        return f'Drop schema {self.name}'
