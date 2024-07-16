from abc import ABC
from typing import Iterable, Optional

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState


class SchemaAccessOperation(ABC, Operation):
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
        self.accesses = ', '.join(access.upper() for access in accesses)
        self.schemas = ', '.join(f'"{schema}"' for schema in schemas)
        self.roles = ', '.join(f'"{role}"' for role in roles)

    def state_forwards(self, app_label: str, state: ProjectState) -> None:
        pass


class GrantSchemaAccess(SchemaAccessOperation):
    """
    Grant access to a given schema.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: Optional[ProjectState] = None, to_state: Optional[ProjectState] = None,
    ) -> None:
        schema_editor.execute(f'GRANT {self.accesses} ON SCHEMA {self.schemas} TO {self.roles}')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: Optional[ProjectState] = None, to_state: Optional[ProjectState] = None,
    ) -> None:
        schema_editor.execute(f'REVOKE {self.accesses} ON SCHEMA {self.schemas} FROM {self.roles}')

    def describe(self) -> str:
        return f'Grant access on {self.schemas} to {self.roles}'


class RevokeSchemaAccess(SchemaAccessOperation):
    """
    Revoke access from a given schema.
    """
    def database_forwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: Optional[ProjectState] = None, to_state: Optional[ProjectState] = None,
    ) -> None:
        schema_editor.execute(f'REVOKE {self.accesses} ON SCHEMA {self.schemas} FROM {self.roles}')

    def database_backwards(
        self, app_label: str, schema_editor: SchemaEditor,
        from_state: Optional[ProjectState] = None, to_state: Optional[ProjectState] = None,
    ) -> None:
        schema_editor.execute(f'GRANT {self.accesses} ON SCHEMA {self.schemas} TO {self.roles}')

    def describe(self) -> str:
        return f'Revoke access on {self.schemas} from {self.roles}'
