from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from tests.static_site.models import SITE


def update_site(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,  # pylint: disable=unused-argument
) -> None:  # pragma: no cover, executed during test setup and tested in the sitemap
    Site = apps.get_model('sites', 'Site')  # pylint: disable=invalid-name
    Site.objects.update_or_create(id=1, defaults=SITE)


class Migration(migrations.Migration):
    dependencies = [
        ('static_site', '0001_initial'),
        ('sites', '0001_initial'),
    ]
    operations = [migrations.RunPython(code=update_site, reverse_code=migrations.RunPython.noop)]
