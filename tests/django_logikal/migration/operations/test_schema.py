from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from pytest import mark

from django_logikal.migration import operations
from tests.django_logikal.migration.operations.utils import has_schema_privilege


def create_schema_and_user(
    schema_editor: SchemaEditor,
    schema: str,
    user_name: str,
) -> None:
    schema_migration = operations.CreateSchema(name=schema)
    schema_migration.database_forwards(app_label='test', schema_editor=schema_editor)

    user_migration = operations.CreateUser(name=user_name, exists_ok=True)
    user_migration.database_forwards(app_label='test', schema_editor=schema_editor)


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


def schema_exists(name: str, schema_editor: SchemaEditor) -> bool:
    with schema_editor.connection.cursor() as cursor:
        sql = 'SELECT 1 FROM information_schema.schemata WHERE schema_name=%(name)s'
        cursor.execute(sql=sql, params={'name': name})
        return bool(cursor.fetchone() == (1, ))


@mark.django_db
def test_create_schema(schema_editor: SchemaEditor) -> None:
    name = 'test_create_schema'

    # Create schema (forwards)
    migration = operations.CreateSchema(name=name)
    migration.database_forwards(app_label='test', schema_editor=schema_editor)
    assert schema_exists(name=name, schema_editor=schema_editor)

    # Create schema (backwards)
    migration.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not schema_exists(name=name, schema_editor=schema_editor)


@mark.django_db
def test_drop_schema(schema_editor: SchemaEditor) -> None:
    name = 'test_drop_schema'

    # Create schema
    create = operations.CreateSchema(name=name)
    create.database_forwards(app_label='test', schema_editor=schema_editor)
    assert schema_exists(name=name, schema_editor=schema_editor)

    # Drop schema
    drop = operations.DropSchema(name=name)
    drop.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not schema_exists(name=name, schema_editor=schema_editor)
