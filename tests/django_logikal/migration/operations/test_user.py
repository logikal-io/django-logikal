from threading import Thread

from django.db import ProgrammingError
from django.db.backends.base.schema import BaseDatabaseSchemaEditor as SchemaEditor
from psycopg import Connection, connect, sql
from psycopg.rows import TupleRow
from pytest import mark, raises

from django_logikal.migration import operations


def user_exists(name: str, schema_editor: SchemaEditor) -> bool:
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql='SELECT 1 FROM pg_roles WHERE rolname=%(name)s', params={'name': name})
        return bool(cursor.fetchone() == (1, ))


def commit_when_blocking(connection: Connection[TupleRow]) -> None:
    # Wait (at most 10 seconds) until another session waits for the current transaction
    connection.execute("""
        DO $$
        BEGIN
          FOR attempt IN 1..1000 LOOP
            EXIT WHEN EXISTS (
              SELECT FROM pg_locks
              WHERE NOT granted AND pg_backend_pid() = ANY(pg_blocking_pids(pid))
            );
            PERFORM pg_sleep(0.01);
          END LOOP;
        END
        $$
    """)
    connection.commit()


@mark.django_db
def test_create_user(schema_editor: SchemaEditor) -> None:
    name = 'test_create_user'
    password = "test_password'\""  # nosec: only used for testing

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
def test_create_user_concurrently(schema_editor: SchemaEditor) -> None:
    name = 'test_create_user_concurrently'
    settings = schema_editor.connection.settings_dict

    # Start creating the same user from another database (users are shared by all databases)
    with connect(
        host=settings['HOST'], port=settings['PORT'], dbname='postgres',
        user=settings['USER'], password=settings['PASSWORD'],
    ) as other_connection:
        other_connection.execute(sql.SQL('CREATE USER {}').format(sql.Identifier(name)))
        commit = Thread(target=commit_when_blocking, args=(other_connection, ))
        commit.start()

        # Create user while the other creation is in progress
        try:
            migration = operations.CreateUser(name=name, exists_ok=True)
            migration.database_forwards(app_label='test', schema_editor=schema_editor)
            assert user_exists(name=name, schema_editor=schema_editor)
        finally:
            commit.join()
            other_connection.execute(sql.SQL('DROP USER {}').format(sql.Identifier(name)))
            other_connection.commit()


@mark.django_db
def test_create_user_error(schema_editor: SchemaEditor) -> None:
    migration = operations.CreateUser(name='pg_test_create_user')
    with raises(ProgrammingError, match='reserved'):
        migration.database_forwards(app_label='test', schema_editor=schema_editor)


@mark.django_db
def test_drop_user(schema_editor: SchemaEditor) -> None:
    name = 'test_drop_user'
    password = "test_password'\""  # nosec: only used for testing

    # Create user
    create = operations.CreateUser(name=name, password=password, exists_ok=False)
    create.database_forwards(app_label='test', schema_editor=schema_editor)
    assert user_exists(name=name, schema_editor=schema_editor)

    # Drop user
    drop = operations.DropUser(name=name)
    drop.database_forwards(app_label='test', schema_editor=schema_editor)
    assert not user_exists(name=name, schema_editor=schema_editor)
