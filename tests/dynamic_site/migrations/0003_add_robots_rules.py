from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def add_rules(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,  # pylint: disable=unused-argument
) -> None:
    Url = apps.get_model('robots', 'Url')  # pylint: disable=invalid-name
    urls = {
        'admin': Url(id=1, pattern='/admin/'),
        'internal': Url(id=2, pattern='/internal/'),
    }
    Url.objects.bulk_create(
        urls.values(), unique_fields=['id'], update_fields=['pattern'], update_conflicts=True,
    )

    Site = apps.get_model('sites', 'Site')  # pylint: disable=invalid-name
    Rule = apps.get_model('robots', 'Rule')  # pylint: disable=invalid-name
    rule = Rule.objects.update_or_create(id=1, defaults={'robot': '*'})[0]
    rule.disallowed.add(*urls.values())
    rule.sites.add(Site.objects.get(domain='logikal.io'))


class Migration(migrations.Migration):
    dependencies = [
        ('dynamic_site', '0002_update_site'),
        ('sites', '0001_initial'),
        ('robots', '0001_initial'),
    ]
    operations = [migrations.RunPython(code=add_rules, reverse_code=migrations.RunPython.noop)]
