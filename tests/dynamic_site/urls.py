from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from rest_framework import urls as rest_framework_auth_urls
from rest_framework.routers import DefaultRouter as APIRouter

from django_logikal.sitemap import StaticSitemap
from django_logikal.templates import Template
from django_logikal.urls import utility_paths
from django_logikal.views import ERROR_HANDLERS, public, redirect_to
from tests.dynamic_site import models, views


class TemplateWithContext(Template):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        request = self.request  # type: ignore[attr-defined] # pylint: disable=no-member
        return {'get_context_data': 'context', 'get_context_data_request': request}


app_name = 'dynamic_site'
template = TemplateWithContext(app=app_name, extra_context={'extra_template_data': 'template'})
template_localized = Template(app=f'{app_name}_localized')

handler400 = ERROR_HANDLERS[400]
handler403 = ERROR_HANDLERS[403]
handler404 = ERROR_HANDLERS[404]
handler500 = ERROR_HANDLERS[500]

api_router = APIRouter()
api_router.register('projects', models.ProjectViewSet)

urlpatterns = [
    # Non-localized URLs
    path('', template.include([
        template.path('', name='index', public=True, priority='1'),
        path('models/', views.ListProjects.as_view(), name='models'),
        template.path(
            'jinja/', name='jinja', public=True, priority='0.5',
            extra_context={'extra_view_data': 'view'},
        ),
        template.path('internal/', name='internal'),
        template.path('invalid-html/', name='invalid-html', public=True),
        path('redirect/', public(redirect_to('dynamic_site:index')), name='redirect'),
        path('email/', views.EmailView.as_view(), name='email'),
    ])),
    # Localized URLs
    *i18n_patterns(
        path('', template_localized.include([
            template_localized.path(
                _('localization/'), name='localization', public=True, priority='0.5',
                extra_context={
                    'date': date(2023, 7, 1),
                    'timestamp': datetime(2023, 7, 1, 14, 34, 56, tzinfo=timezone.utc),
                    'number': Decimal('42010.12345'),
                    'currency': Decimal('105432.12345'),
                    # Note: we use a lambda to make sure the active language is used
                    # Translators: This is a view test comment for translators
                    'localized_view_data': lambda: _('localized %(word)s') % {
                        'word': _('marvelous'),
                    }
                },
            ),
        ])),
    ),
    # API
    path('api/', include(api_router.urls)),
    path('api/auth/', include(rest_framework_auth_urls)),
    # Utilities
    *utility_paths(sitemaps={
        'template': template.sitemap(),
        'template_localized': template_localized.sitemap(),
        'models': StaticSitemap({'dynamic_site:models': '0.75'})
    }),
]
