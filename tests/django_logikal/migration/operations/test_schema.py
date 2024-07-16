from typing import cast

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from pytest import mark

from django_logikal.migration import operations


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


def create_schema_and_user(
    schema_editor: SchemaEditor,
    schema: str,
    user_name: str,
) -> None:
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA {schema}')

    migration = operations.CreateUser(name=user_name, exists_ok=True)
    migration.database_forwards(app_label='test', schema_editor=schema_editor)


@mark.django_db
def test_grant_schema_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_grant_schema_access'
    schema = 'test_grant_schema_access'

    create_schema_and_user(schema_editor, schema=schema, user_name=user_name)

    # Grant access (forwards)
    assert not has_schema_privilege(schema_editor, user_name=user_name, schema=schema)
    grant = operations.GrantSchemaAccess(schemas=[schema], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)
    assert has_schema_privilege(schema_editor, user_name=user_name, schema=schema)

    # Grant access (backwards)
    grant.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not has_schema_privilege(schema_editor, user_name=user_name, schema=schema)


@mark.django_db
def test_revoke_schema_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_revoke_schema_access'
    schema = 'test_revoke_schema_access'

    create_schema_and_user(schema_editor, schema=schema, user_name=user_name)

    # Grant access
    grant = operations.GrantSchemaAccess(schemas=[schema], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)

    # Revoke access (forwards)
    assert has_schema_privilege(schema_editor, user_name=user_name, schema=schema)
    revoke = operations.RevokeSchemaAccess(schemas=[schema], roles=[user_name])
    revoke.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not has_schema_privilege(schema_editor, user_name=user_name, schema=schema)

    # Revoke access (backwards)
    revoke.database_backwards(app_label='test', schema_editor=schema_editor)
    assert has_schema_privilege(schema_editor, user_name=user_name, schema=schema)
