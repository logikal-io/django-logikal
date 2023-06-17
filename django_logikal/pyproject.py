from pathlib import Path

import tomli

PYPROJECT = (
    tomli.loads(Path('pyproject.toml').read_text(encoding='utf-8'))
    if Path('pyproject.toml').exists() else {}
)
DJANGO_LOGIKAL_CONFIG = PYPROJECT.get('tool', {}).get('django_logikal', {})
