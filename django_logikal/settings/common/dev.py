from logikal_utils.docker import Service

from django_logikal.env import get_option, option_is_set
from django_logikal.logging import logging_config
from django_logikal.settings import Settings, SettingsUpdate


class CommonDevSettings(SettingsUpdate):
    # Logging
    LOGGING = logging_config(
        log_level=get_option('log_level', 'INFO'),
        console=True,
        cloud=option_is_set('cloud_logging'),
    )

    # Security
    SECRET_KEY = 'dev'  # nosec: only used for development

    # Core settings
    DEBUG = option_is_set('dev_run')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': '127.0.0.1',
            'PORT': Service('postgres').container_port('5432/tcp'),
            'NAME': 'dev',
            'USER': 'dev',
            'PASSWORD': 'dev',
        },
    }

    # Migration linter
    MIGRATION_LINTER_OPTIONS = {'exclude_apps': ['sites', 'robots']}
    MIGRATION_LINTER_OVERRIDE_MAKEMIGRATIONS = True

    @staticmethod
    def apply(settings: Settings) -> None:
        # HTML validation
        settings['MIDDLEWARE'] += ['django_logikal.validation.ValidationMiddleware']

        # Migration linter
        settings['INSTALLED_APPS'] += ['django_migration_linter']

        # Debug toolbar
        if option_is_set('toolbar'):  # pragma: no cover, tested in subprocess
            settings['MIDDLEWARE'].insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
            settings['CSP_DEFAULT_SRC'] += " 'nonce-debug-toolbar'"
            settings['INSTALLED_APPS'] += ['debug_toolbar', 'template_profiler_panel']
            settings['INTERNAL_IPS'] = ['127.0.0.1']
            settings['DEBUG_TOOLBAR_PANELS'] = [
                'debug_toolbar.panels.history.HistoryPanel',
                'debug_toolbar.panels.timer.TimerPanel',
                'debug_toolbar.panels.settings.SettingsPanel',
                'debug_toolbar.panels.headers.HeadersPanel',
                'debug_toolbar.panels.request.RequestPanel',
                'debug_toolbar.panels.sql.SQLPanel',
                'template_profiler_panel.panels.template.TemplateProfilerPanel',
                'debug_toolbar.panels.staticfiles.StaticFilesPanel',
                'debug_toolbar.panels.cache.CachePanel',
                'debug_toolbar.panels.signals.SignalsPanel',
                'debug_toolbar.panels.redirects.RedirectsPanel',
                'debug_toolbar.panels.profiling.ProfilingPanel',
            ]
            settings['DEBUG_TOOLBAR_CONFIG'] = {
                'SHOW_COLLAPSED': True,
                'TOOLBAR_LANGUAGE': 'en-us',
                'SQL_WARNING_THRESHOLD': 100,  # milliseconds
                'DISABLE_PANELS': {
                    'debug_toolbar.panels.signals.SignalsPanel',
                    'debug_toolbar.panels.redirects.RedirectsPanel',
                    'debug_toolbar.panels.profiling.ProfilingPanel',
                },
            }
            if 'EMAIL_BACKEND' in settings:
                settings['INSTALLED_APPS'] += ['mail_panel']
                settings['EMAIL_BACKEND'] = 'mail_panel.backend.MailToolbarBackend'
                settings['DEBUG_TOOLBAR_PANELS'].insert(0, 'mail_panel.panels.MailToolbarPanel')
