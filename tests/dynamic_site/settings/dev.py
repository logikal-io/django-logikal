from django_logikal.settings import Settings
from django_logikal.settings.dynamic_site.dev import DevSettings
from tests.dynamic_site.settings.app import AppSettings

Settings(globals()).update(DevSettings).update(AppSettings)
