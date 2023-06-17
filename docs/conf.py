import os
import sys
from importlib.metadata import version as pkg_version

from sphinx.addnodes import desc_signature, document
from sphinx.application import Sphinx

from django_logikal.pyproject import DJANGO_LOGIKAL_CONFIG

sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_LOGIKAL_CONFIG['DJANGO_SETTINGS_MODULE']


def strip_patch(package: str) -> str:
    return '.'.join(pkg_version(package).split('.')[0:2])  # major.minor (excluding patch)


extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': (f'https://docs.python.org/{sys.version_info[0]}.{sys.version_info[1]}', None),
    'django': (
        f'https://docs.djangoproject.com/en/{strip_patch("django")}/',
        f'https://docs.djangoproject.com/en/{strip_patch("django")}/_objects/',
    ),
    'babel': ('https://babel.pocoo.org/en/latest/', None),
    'jinja2': (f'https://jinja.palletsprojects.com/en/{strip_patch("jinja2")}.x/', None),
    'django-robots': ('https://django-robots.readthedocs.io/en/latest/', None),
    'django-anymail': (f'https://anymail.dev/en/v{pkg_version("django-anymail")}/', None),
    'factory-boy': (f'https://factoryboy.readthedocs.io/en/{pkg_version("factory-boy")}/', None),
    'stormware': (f'https://docs.logikal.io/stormware/{pkg_version("stormware")}/', None),
}

nitpick_ignore = [
    ('py:func', 'type'),
    ('py:class', 'django.conf.LazySettings'),
    ('py:class', 'django.http.request.HttpRequest'),
    ('py:class', 'django.http.response.HttpResponse'),
    ('py:class', 'django.http.response.HttpResponseBase'),
    ('py:class', 'django.http.response.HttpResponseNotFound'),
    ('py:class', 'django.http.response.HttpResponseServerError'),
    ('py:class', 'django.urls.resolvers.URLResolver'),
    ('py:class', 'django.urls.resolvers.URLPattern'),
    ('py:class', 'django.core.management.base.CommandParser'),
]


def strip_modules(
    app: Sphinx,  # pylint: disable=unused-argument
    doctree: document,
) -> None:  # pragma: no cover
    modules = set([
        'django_logikal.templates.filters',
        'django_logikal.templates.tests',
        'django_logikal.templates.functions',
    ])
    for signature in doctree.findall(desc_signature):
        if signature.get('module') in modules:
            del signature[0]  # remove module text


def setup(app: Sphinx) -> None:
    app.connect('doctree-read', strip_modules)
