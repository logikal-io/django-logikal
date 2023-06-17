from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from django_logikal.templates import Template
from django_logikal.urls import utility_paths

template = Template()

urlpatterns = [
    template.static_path('', name='index', priority='1'),
    template.static_path('test/', name='test', priority='0.75'),
    *i18n_patterns(template.static_path(_('localization/'), name='localization', priority='0.5')),
    *utility_paths(sitemaps={'sitemap': template.sitemap()}, static=True),
]
