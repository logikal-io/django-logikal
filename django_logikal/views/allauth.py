from typing import Any

from allauth.account import views
from django.http import HttpResponse
from django.urls import reverse_lazy

from django_logikal.forms.allauth import (
    ChangePasswordForm, LoginForm, ResetPasswordForm,
    ResetPasswordKeyForm, SetPasswordForm, SignupForm,
)
from django_logikal.views.generic import HTMXFormView, PublicViewMixin


class SignupView(PublicViewMixin, HTMXFormView[SignupForm], views.SignupView):
    """
    View for signing a user up.
    """
    def get_initial(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        initial = super().get_initial()
        if email := self.request.session.get('email'):
            initial['email'] = email
        return initial

    def form_valid(self, form: SignupForm) -> HttpResponse:  # noqa: D400, D415
        """
        :meta private:
        """
        email = form.cleaned_data['email']
        self.request.session['email'] = email
        return super().form_valid(form=form)


class LoginView(PublicViewMixin, HTMXFormView[LoginForm], views.LoginView):
    """
    View for logging a user in.
    """
    def get_initial(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        initial = super().get_initial()
        if email := self.request.session.get('email'):
            initial['login'] = email
        return initial


class PasswordResetView(PublicViewMixin, HTMXFormView[ResetPasswordForm], views.PasswordResetView):
    """
    Show the password reset form.
    """
    def get_initial(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        initial = super().get_initial()
        if email := self.request.session.get('email'):
            initial['email'] = email
        return initial

    def form_valid(self, form: ResetPasswordForm) -> HttpResponse:  # noqa: D400, D415
        """
        :meta private:
        """
        email = form.cleaned_data['email']
        self.request.session['email'] = email
        return super().form_valid(form=form)


class PasswordResetFromKeyView(
    PublicViewMixin,
    HTMXFormView[ResetPasswordKeyForm], views.PasswordResetFromKeyView,
):
    """
    View for resetting a user's password.
    """
    success_url = reverse_lazy('account_login')

    def get_initial(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        initial = super().get_initial()
        if email := self.request.session.get('email'):
            initial['email'] = email
        return initial

    def get_form_kwargs(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        kwargs = super().get_form_kwargs()
        kwargs['action_url_kwargs'] = {'uidb36': self.kwargs['uidb36'], 'key': self.kwargs['key']}
        return kwargs


class PasswordSetView(HTMXFormView[SetPasswordForm], views.PasswordSetView):
    """
    View for setting the user's password.
    """


class PasswordChangeView(HTMXFormView[ChangePasswordForm], views.PasswordChangeView):
    """
    View for changing the user's password.
    """
