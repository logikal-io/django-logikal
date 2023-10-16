from django_logikal.env import set_option
from django_logikal.logging import logging_config
from django_logikal.settings import Settings, SettingsUpdate


class CommonTestingSettings(SettingsUpdate):
    LOGGING = logging_config(console=False)  # logs are captured by pytest already

    @staticmethod
    def apply(settings: Settings) -> None:
        settings['STORAGES']['staticfiles'] = {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        }

        # Custom settings
        set_option('testing')
