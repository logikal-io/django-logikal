from django_logikal.settings import Settings
from django_logikal.settings.dynamic_site.production import ProductionSettings
from tests.dynamic_site.settings.app import AppSettings

Settings(globals()).update(ProductionSettings).update(AppSettings)
