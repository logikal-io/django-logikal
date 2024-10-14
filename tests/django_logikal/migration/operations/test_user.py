from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from pytest import mark, raises

from django_logikal.migration import operations


def user_exists(name: str, schema_editor: SchemaEditor) -> bool:
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql='SELECT 1 FROM pg_roles WHERE rolname=%(name)s', params={'name': name})
        return bool(cursor.fetchone() == (1, ))


@mark.django_db
def test_create_user(schema_editor: SchemaEditor) -> None:
    name = 'test_create_user'
    password = 'test_password'  # nosec: only used for testing

    # Create user (forwards)
    migration = operations.CreateUser(name=name, password=password, exists_ok=False)
    migration.database_forwards(app_label='test', schema_editor=schema_editor)
    assert user_exists(name=name, schema_editor=schema_editor)

    # Existing user (no error)
    migration = operations.CreateUser(name=name, password=password, exists_ok=True)
    migration.database_forwards(app_label='test', schema_editor=schema_editor)
    assert user_exists(name=name, schema_editor=schema_editor)

    # Existing user (error)
    migration = operations.CreateUser(name=name, password=password, exists_ok=False)
    with raises(RuntimeError, match='already exists'):
        migration.database_forwards(app_label='test', schema_editor=schema_editor)

    # Create user (backwards)
    migration.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not user_exists(name=name, schema_editor=schema_editor)


@mark.django_db
def test_drop_user(schema_editor: SchemaEditor) -> None:
    name = 'test_drop_user'
    password = 'test_password'  # nosec: only used for testing

    # Create user
    create = operations.CreateUser(name=name, password=password, exists_ok=False)
    create.database_forwards(app_label='test', schema_editor=schema_editor)
    assert user_exists(name=name, schema_editor=schema_editor)

    # Drop user
    drop = operations.DropUser(name=name)
    drop.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not user_exists(name=name, schema_editor=schema_editor)
