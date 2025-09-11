from abc import ABC
from collections.abc import Iterable

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState
from django.db.models import Model


class ModelAccessOperation(ABC, Operation):
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

        self.accesses = ', '.join(access.upper() for access in accesses)
        self.tables = ', '.join(f'"{table}"' for table in tables)
        self.roles = ', '.join(f'"{role}"' for role in roles)

    def state_forwards(self, app_label: str, state: ProjectState) -> None:
        pass


class GrantModelAccess(ModelAccessOperation):
    """
    Grant access to a given set of models.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        schema_editor.execute(f'GRANT {self.accesses} ON {self.tables} TO {self.roles}')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        schema_editor.execute(f'REVOKE {self.accesses} ON {self.tables} FROM {self.roles}')

    def describe(self) -> str:
        return f'Grant access on {self.tables} to {self.roles}'


class RevokeModelAccess(ModelAccessOperation):
    """
    Revoke access from a given set of models.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        schema_editor.execute(f'REVOKE {self.accesses} ON {self.tables} FROM {self.roles}')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: ProjectState | None = None, to_state: ProjectState | None = None,
    ) -> None:
        schema_editor.execute(f'GRANT {self.accesses} ON {self.tables} TO {self.roles}')

    def describe(self) -> str:
        return f'Revoke access on {self.tables} from {self.roles}'
