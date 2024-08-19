from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from pytest import mark

from django_logikal.migration import operations
from tests.django_logikal.migration.operations.utils import has_table_privilege
from tests.dynamic_site.models import User


@mark.django_db
def test_grant_table_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_grant_table_access'
    table = User._meta.db_table

    create = operations.CreateUser(name=user_name, exists_ok=True)
    create.database_forwards(app_label='test', schema_editor=schema_editor)

    # Grant access (forwards)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)
    grant = operations.GrantTableAccess(tables=[table], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)

    # Grant access (backwards)
    grant.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)


@mark.django_db
def test_grant_all_table_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_grant_all_table_access'
    table = User._meta.db_table

    create = operations.CreateUser(name=user_name, exists_ok=True)
    create.database_forwards(app_label='test', schema_editor=schema_editor)

    # Grant access (forwards)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)
    grant = operations.GrantTableAccess(tables=['ALL TABLES IN SCHEMA public'], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)

    # Grant access (backwards)
    grant.database_backwards(app_label='test', schema_editor=schema_editor)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)


@mark.django_db
def test_revoke_table_access(schema_editor: SchemaEditor) -> None:
    user_name = 'test_revoke_table_access'
    table = User._meta.db_table

    create = operations.CreateUser(name=user_name, exists_ok=True)
    create.database_forwards(app_label='test', schema_editor=schema_editor)

    # Grant access
    grant = operations.GrantTableAccess(tables=[table], roles=[user_name])
    grant.database_forwards(app_label='test', schema_editor=schema_editor)

    # Revoke access (forwards)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)
    revoke = operations.RevokeTableAccess(tables=[table], roles=[user_name])
    revoke.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not has_table_privilege(schema_editor, user_name=user_name, table=table)

    # Revoke access (backwards)
    revoke.database_backwards(app_label='test', schema_editor=schema_editor)
    assert has_table_privilege(schema_editor, user_name=user_name, table=table)
