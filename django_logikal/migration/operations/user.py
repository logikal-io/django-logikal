from django.db import IntegrityError, ProgrammingError, transaction
from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.state import ProjectState
from psycopg import sql
from psycopg.errors import DuplicateObject, UniqueViolation

from django_logikal.migration.operations.base import SQLOperation


class UserOperation(SQLOperation):
    def __init__(self, name: str):  # noqa: D205, D400, D415
        """
        Args:
            name: The user name to use.

        """
        self.name = name


class CreateUser(UserOperation):
    def __init__(
        self,
        name: str,
        password: str | None = None,
        exists_ok: bool = False,
    ):
        """
        Create a user.

        Args:
            name: The user name to use.
            password: The password to use.
            exists_ok: Whether to suppress errors related to a user already existing.

        """
        super().__init__(name=name)
        self.password = password
        self.exists_ok = exists_ok

    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        connection = schema_editor.connection
        with connection.cursor() as cursor:
            cursor.execute(
                sql='SELECT 1 FROM pg_roles WHERE rolname=%(name)s',
                params={'name': self.name},
            )
            user_exists = bool(cursor.fetchone())

        if not user_exists:
            statement = sql.SQL('CREATE USER {}').format(sql.Identifier(self.name))
            params: tuple[object, ...] = ()
            if self.password:
                statement += sql.SQL(' WITH PASSWORD %s')
                params = (self.password, )
            try:
                with transaction.atomic(using=connection.alias):
                    self.execute_statement(schema_editor, statement=statement, params=params)
            except (IntegrityError, ProgrammingError) as error:
                if not isinstance(error.__cause__, (DuplicateObject, UniqueViolation)):
                    raise
                user_exists = True

        if user_exists and not self.exists_ok:
            raise RuntimeError(f'User "{self.name}" already exists')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('DROP USER {}').format(sql.Identifier(self.name))
        self.execute_statement(schema_editor, statement=statement)

    def describe(self) -> str:
        return f'Create user {self.name}'


class DropUser(UserOperation):
    """
    Drop a user.
    """
    reversible = False

    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        statement = sql.SQL('DROP USER IF EXISTS {}').format(sql.Identifier(self.name))
        self.execute_statement(schema_editor, statement=statement)

    def describe(self) -> str:
        return f'Drop user {self.name}'
