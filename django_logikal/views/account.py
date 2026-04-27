from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django_logikal.templates.functions import url

from django_logikal.views.generic import PublicViewMixin


class AuthView(PublicViewMixin, TemplateView):
    template_name = 'account/auth.html.j'

    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Authenticate a user.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def get_context_data(self) -> dict[str, Any]:
        return {
            'provider_login_urls': {
                provider: url(
                    provider_module + '_login', request=self.request,
                    request_get_update={'process': 'login'},
                )
                for provider_module, provider in settings.ALLAUTH_SOCIAL_PROVIDERS.items()
            }
        }

    def post(self, request: HttpRequest) -> HttpResponse:
        if not (email := request.POST.get('email')):
            return self.get(request=request)

        request.session['email'] = email
        user = get_user_model()
        if user.objects.filter(email=email).exists():
            return redirect(url('account_login', request=request))

        return redirect(url('account_signup', request=request))


class AccountView(TemplateView):
    template_name = 'account/account.html.j'

    def get_context_data(self) -> dict[str, Any]:
        return {'social_accounts': self.request.user.socialaccount_set.all()}
