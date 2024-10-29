from abc import ABC
from typing import Any

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState


class UserOperation(ABC, Operation):
    def __init__(self, name: str):  # noqa: D205, D400, D415
        """
        Args:
            name: The user name to use.

        """
        self.name = name

    def state_forwards(self, app_label: str, state: ProjectState) -> None:
        pass


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
        with schema_editor.connection.cursor() as cursor:
            cursor.execute(
                sql='SELECT 1 FROM pg_roles WHERE rolname=%(name)s',
                params={'name': self.name},
            )
            user_exists = bool(cursor.fetchone())
        if not user_exists:
            sql = f'CREATE USER "{self.name}"'
            params: Any = {}
            if self.password:
                sql += ' WITH PASSWORD %(password)s'
                params['password'] = self.password
            schema_editor.execute(sql=sql, params=params)
        elif not self.exists_ok:
            raise RuntimeError(f'User "{self.name}" already exists')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        schema_editor.execute(f'DROP USER "{self.name}"')

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
        schema_editor.execute(f'DROP USER IF EXISTS "{self.name}"')

    def describe(self) -> str:
        return f'Drop user {self.name}'
