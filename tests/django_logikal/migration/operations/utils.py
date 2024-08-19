from typing import cast

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor


def has_schema_privilege(
    schema_editor: SchemaEditor,
    user_name: str,
    schema: str,
) -> bool:
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            sql="SELECT has_schema_privilege(%(user_name)s, %(schema)s, 'usage')",
            params={'user_name': user_name, 'schema': schema},
        )
        return cast(bool, cursor.fetchone()[0])


def has_table_privilege(
    schema_editor: SchemaEditor,
    user_name: str,
    table: str,
) -> bool:
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            sql="SELECT has_table_privilege(%(user_name)s, %(table)s, 'select')",
            params={'user_name': user_name, 'table': table},
        )
        return cast(bool, cursor.fetchone()[0])
