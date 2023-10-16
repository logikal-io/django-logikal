from django_logikal.settings import Settings
from django_logikal.settings.dynamic_site.testing import TestingSettings
from tests.dynamic_site.settings.app import AppSettings

Settings(globals()).update(TestingSettings).update(AppSettings)
