# pylint: disable=wildcard-import, unused-wildcard-import
import os
from pathlib import Path

from django_logikal.settings.base import *

# Security
SECRET_KEY = 'static'  # nosec: not used for static sites (but still has to be set)

# Core settings
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']  # variants of localhost
INSTALLED_APPS += ['django_distill']

# Static site generation
DISTILL_DIR = Path(os.getcwd()) / 'generated'
