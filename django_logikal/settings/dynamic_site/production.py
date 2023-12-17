from django_logikal.settings.common.production import CommonProductionSettings
from django_logikal.settings.dynamic_site.base import BaseSettings


class ProductionSettings(BaseSettings, CommonProductionSettings):
    """
    Standard production settings for dynamic sites.

    .. note:: Secrets will be loaded from Google Secret Manager during import time. In particular,
        the secret key is loaded from the ``SECRET_KEY_PATH`` setting key (defaults to
        ``{project}-website-secret-key``, where ``{project}`` is the project name in the
        ``pyproject.toml`` file), and the database configuration is loaded from the
        ``DATABASE_SECRETS_PATH`` setting key (defaults to ``{project}-website-database-secrets``),
        which must contain a JSON string with keys ``hostname``, ``port``, ``database``,
        ``username`` and ``password``.
    """
