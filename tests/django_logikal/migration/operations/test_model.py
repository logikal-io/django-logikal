from typing import cast

from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from pytest import mark

from django_logikal.migration import operations
from tests.dynamic_site.models import User


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


@mark.django_db
def test_grant_model_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_grant_model_access'
    model = User
    table = User._meta.db_table

    create = operations.CreateUser(name=user_name, exists_ok=True)
    create.database_forwards(app_label='test', schema_editor=schema_editor)

    # Grant access (forwards)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)
    grant = operations.GrantModelAccess(models=[model], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)

    # Grant access (backwards)
    grant.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)


@mark.django_db
def test_revoke_model_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_revoke_model_access'
    model = User
    table = User._meta.db_table

    create = operations.CreateUser(name=user_name, exists_ok=True)
    create.database_forwards(app_label='test', schema_editor=schema_editor)

    # Grant access
    grant = operations.GrantModelAccess(models=[model], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)

    # Revoke access (forwards)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)
    revoke = operations.RevokeModelAccess(models=[model], roles=[user_name])
    revoke.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)

    # Revoke access (backwards)
    revoke.database_backwards(app_label='test', schema_editor=schema_editor)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)
