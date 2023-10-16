from django_logikal.settings.common.testing import CommonTestingSettings
from django_logikal.settings.dynamic_site.dev import DevSettings


class TestingSettings(CommonTestingSettings, DevSettings):
    """
    Standard settings for testing dynamic sites.
    """
