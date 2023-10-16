from django_logikal.settings.common.testing import CommonTestingSettings
from django_logikal.settings.static_site.dev import DevSettings


class TestingSettings(CommonTestingSettings, DevSettings):
    """
    Standard settings for testing static sites.
    """
