from django.db import migrations

from django_logikal.migration import operations
from tests.dynamic_site.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_site', '0003_add_robots_rules'),
    ]
    operations = [
        # Forwards
        operations.CreateSchema(name='test_schema'),  # nosec
        operations.CreateUser(name='test_user', password='test_password', exists_ok=True),  # nosec
        operations.GrantSchemaAccess(schemas=['test_schema'], roles=['test_user']),
        operations.GrantModelAccess(models=[User], roles=['test_user']),
        operations.GrantTableAccess(tables=[User._meta.db_table], roles=['test_user']),

        # Backwards
        operations.RevokeTableAccess(tables=[User._meta.db_table], roles=['test_user']),
        operations.RevokeModelAccess(models=[User], roles=['test_user']),
        operations.RevokeSchemaAccess(schemas=['test_schema'], roles=['test_user']),
        operations.DropUser(name='test_user'),
        operations.DropSchema(name='test_schema'),
    ]
