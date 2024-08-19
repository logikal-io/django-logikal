from django.db import migrations

from django_logikal.migration import operations
from tests.dynamic_site.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_site', '0003_add_robots_rules'),
    ]
    operations = [
        # Forwards
        operations.CreateUser(name='test_user', password='test_password', exists_ok=True),  # nosec
        operations.GrantSchemaAccess(schemas=['public'], roles=['test_user']),
        operations.GrantModelAccess(models=[User], roles=['test_user']),
        operations.GrantTableAccess(tables=[User._meta.db_table], roles=['test_user']),

        # Backwards
        operations.RevokeTableAccess(tables=[User._meta.db_table], roles=['test_user']),
        operations.RevokeModelAccess(models=[User], roles=['test_user']),
        operations.RevokeSchemaAccess(schemas=['public'], roles=['test_user']),
        operations.DropUser(name='test_user'),
    ]
