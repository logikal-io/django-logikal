from django_logikal.env import set_option
from django_logikal.logging import logging_config

LOGGING = logging_config(console=False)  # logs are captured by pytest already
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}

# Custom settings
set_option('testing')
