from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.http import HttpRequest
from django.urls import reverse

from django_logikal.models.base import BaseUser


class AccountAdapter(DefaultAccountAdapter):
    def get_password_change_redirect_url(self, request: HttpRequest) -> str:
        return reverse('account')


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, Any],
    ) -> BaseUser:
        user = super().populate_user(request=request, sociallogin=sociallogin, data=data)

        # Populate full name
        if not (name := data.get('name')):
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            if first_name and last_name:
                name = f'{first_name} {last_name}'
            else:
                name = first_name or last_name

        user_field(user, 'name', name)
        return user
