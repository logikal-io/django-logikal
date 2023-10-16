from django_logikal.settings import Settings
from django_logikal.settings.static_site.dev import DevSettings
from tests.static_site.settings.app import AppSettings

Settings(globals()).update(DevSettings).update(AppSettings)
