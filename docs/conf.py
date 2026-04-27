import importlib
import os
import sys
from pathlib import Path

from docutils import nodes
from logikal_utils import node
from logikal_utils.project import tool_config
from sphinx import addnodes
from sphinx.application import Sphinx

from docs.jinja.domain import JinjaDomain

sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = tool_config('django_logikal')['DJANGO_SETTINGS_MODULE']


def pkg_version(package_name: str) -> str:
    return importlib.metadata.version(package_name)


def strip_patch(package: str) -> str:
    return '.'.join(pkg_version(package).split('.')[0:2])  # major.minor (excluding patch)


extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
]

intersphinx_mapping = {
    'python': (f'https://docs.python.org/{sys.version_info[0]}.{sys.version_info[1]}', None),
    'django': (f'https://docs.djangoproject.com/en/{strip_patch('django')}/', None),
    'babel': ('https://babel.pocoo.org/en/latest/', None),
    'jinja2': ('https://jinja.palletsprojects.com/en/latest/', None),
    'django-robots': ('https://django-robots.readthedocs.io/en/latest/', None),
    'django-anymail': (f'https://anymail.dev/en/v{pkg_version('django-anymail')}/', None),
    'factory-boy': (f'https://factoryboy.readthedocs.io/en/{pkg_version('factory-boy')}/', None),
    'Faker': ('https://faker.readthedocs.io/en/stable/', None),
    'stormware': (f'https://docs.logikal.io/stormware/{pkg_version('stormware')}/', None),
    'pytest-logikal': (
        f'https://docs.logikal.io/pytest-logikal/{pkg_version('pytest-logikal')}/', None,
    ),
}

nitpick_ignore = [
    ('py:func', 'type'),
    ('ref', 'jinja2.ext.i18n'),
    ('py:class', 'T'),  # type vars do not seem to work quite very well
    ('py:class', 'django.conf.LazySettings'),
    ('py:class', 'django.core.management.base.CommandParser'),
    ('py:class', 'django.db.models.base.Model'),
    ('py:class', 'django.http.request.HttpRequest'),
    ('py:class', 'django.http.response.HttpResponse'),
    ('py:class', 'django.http.response.HttpResponseBase'),
    ('py:class', 'django.http.response.HttpResponseNotFound'),
    ('py:class', 'django.http.response.HttpResponseServerError'),
    ('py:class', 'django.urls.resolvers.URLPattern'),
    ('py:class', 'django.urls.resolvers.URLResolver'),
    ('py:class', 'faker.Faker'),
    ('py:class', 'faker.proxy.Faker'),
]

html_static_path = ['static', '../django_logikal/static']
napoleon_custom_sections = [('CSS variables', 'params_style')]


def strip_modules(
    app: Sphinx,  # pylint: disable=unused-argument
    doctree: nodes.document,
) -> None:  # pragma: no cover
    modules = set([
        'django_logikal.templates.filters',
        'django_logikal.templates.tests',
        'django_logikal.templates.functions',
    ])
    for signature in doctree.findall(addnodes.desc_signature):
        if signature.get('module') in modules:
            del signature[0]  # remove module text


def setup(app: Sphinx) -> None:
    app.connect('doctree-read', strip_modules)
    app.add_domain(JinjaDomain)
    app.add_css_file('css/jinja.css')
    app.add_css_file('css/copybutton.css')
    node.install_packages(prefix=Path(__file__).parent)
