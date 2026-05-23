from typing import Any

from allauth.account import views
from django.http import HttpResponse
from django.urls import reverse_lazy

from django_logikal.forms.allauth import SignupForm
from django_logikal.views.generic import HTMXFormView, PublicViewMixin


class SignupView(PublicViewMixin, HTMXFormView[Any], views.SignupView):  # type: ignore[misc]
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        View for signing a user up.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

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


class LoginView(PublicViewMixin, HTMXFormView[Any], views.LoginView):  # type: ignore[misc]
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        View for logging a user in.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

    def get_initial(self) -> dict[str, Any]:  # noqa: D400, D415
        """
        :meta private:
        """
        initial = super().get_initial()
        if email := self.request.session.get('email'):
            initial['login'] = email
        return initial


class PasswordResetView(
    PublicViewMixin, HTMXFormView[Any], views.PasswordResetView,  # type: ignore[misc]
):
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        Show the password reset form.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

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


class PasswordResetFromKeyView(
    PublicViewMixin, HTMXFormView[Any], views.PasswordResetFromKeyView,  # type: ignore[misc]
):
    success_url = reverse_lazy('account_login')

    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        View for resetting a user's password.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover

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


class PasswordSetView(HTMXFormView[Any], views.PasswordSetView):  # type: ignore[misc]
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        View for setting the user's password.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover


class PasswordChangeView(HTMXFormView[Any], views.PasswordChangeView):  # type: ignore[misc]
    # Note: we redefine init to override the inherited class docstring
    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=useless-parent-delegation
        """
        View for changing the user's password.
        """
        super().__init__(*args, **kwargs)  # pragma: no cover
