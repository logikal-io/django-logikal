from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django_logikal.forms.account import AuthForm
from django_logikal.templates.functions import url
from django_logikal.views.generic import HTMXFormView, PublicViewMixin


class AuthView(PublicViewMixin, HTMXFormView[AuthForm]):  # pylint: disable=too-many-ancestors
    template_name = 'account/auth.html.j'  #: The template to use.
    form_class = AuthForm

    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Show the user authentication form.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def get_context_data(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            **super().get_context_data(*args, **kwargs),
            'provider_login_urls': {
                provider: url(
                    provider_module + '_login', request=self.request,
                    request_get_update={'process': 'login'},
                )
                for provider_module, provider
                in settings.ALLAUTH_SOCIAL_PROVIDERS.items()  # type: ignore[misc]
            }
        }

    def form_valid(self, form: AuthForm) -> HttpResponse:
        email = form.cleaned_data['email']
        self.request.session['email'] = email
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.has_usable_password():
                return redirect(url('account_login', request=self.request))
        except user_model.DoesNotExist:
            user = None

        return redirect(url('account_signup', request=self.request))


class AccountView(TemplateView):
    template_name = 'account/account.html.j'  #: The template to use.

    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Show user account information.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Return the template context.

        Includes the ``social_accounts`` field containing all connected social account instances of
        the user.
        """
        social_accounts = self.request.user.socialaccount_set.all()  # type: ignore[union-attr]
        return {**super().get_context_data(**kwargs), 'social_accounts': social_accounts}
