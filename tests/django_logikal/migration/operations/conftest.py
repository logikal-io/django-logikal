from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from pytest import fixture


@fixture
def schema_editor() -> BaseDatabaseSchemaEditor:
    return BaseDatabaseSchemaEditor(connection=connection)
