# pylint: disable=too-many-ancestors
from typing import Any

from allauth.account import forms
from allauth.utils import set_form_field_order
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_logikal.forms import account, fields, generic


class SignupForm(account.AuthForm, forms.SignupForm):  # type: ignore[misc]
    password1 = fields.PasswordField(
        required=True, label=_('Password'), autocomplete='new-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )

    class Meta(generic.FormMeta):
        id = 'signup'
        action_url_name = 'account_signup'
        action_button_text = _('Sign up')
        back_url_name = 'account_auth'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # We reset the base fields as allauth overrides the originals
        self.fields['email'].label = self.base_fields['email'].label
        self.fields['password1'] = self.base_fields['password1']
        self.add_htmx_validation()


class LoginForm(account.AuthForm, forms.LoginForm):  # type: ignore[misc]
    password = fields.PasswordField(
        required=True, label=_('Password'), autocomplete='current-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )

    class Meta(generic.FormMeta):
        id = 'login'
        action_url_name = 'account_login'
        action_button_text = _('Sign in')
        back_url_name = 'account_auth'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['login'] = self.fields['email']
        del self.fields['email']
        self.add_htmx_validation()


class ResetPasswordForm(account.AuthForm, forms.ResetPasswordForm):  # type: ignore[misc]
    class Meta(generic.FormMeta):
        id = 'reset_password'
        action_url_name = 'account_reset_password'
        header = _('Reset Password')
        help_text = _(
            'Forgot your password? Enter your email address below, '
            'and we will send you a link to set a new password.'
        )
        action_button_text = _('Next')
        back_url_name = 'account_login'


class ResetPasswordKeyForm(generic.Form, forms.ResetPasswordKeyForm):  # type: ignore[misc]
    email = fields.EmailField(
        required=True, label=_('Email address'), placeholder=_('email@example.com'),
        autocomplete='username', spellcheck=False, read_only=True,
    )
    password1 = fields.PasswordField(
        required=True, label=_('New password'), autocomplete='new-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )

    class Meta(generic.FormMeta):
        id = 'reset_password_key'
        action_url_name = 'account_reset_password_from_key'
        header = _('Reset Password')
        action_button_text = _('Set password')
        back_url_name = 'account_login'

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        set_form_field_order(self, ['email', 'password1'])

    def clean(self) -> dict[str, Any] | None:  # noqa: D400, D415
        """
        :meta private:
        """
        if self.data:
            data = self.data.copy()  # type: ignore[attr-defined]
            data['password2'] = data.get('password1')
            self.data = data
        return super().clean()


class SetPasswordForm(generic.Form, forms.SetPasswordForm):  # type: ignore[misc]
    password1 = fields.PasswordField(
        required=True, label=_('New password'), autocomplete='new-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )

    class Meta(generic.FormMeta):
        id = 'set_password'
        action_url_name = 'account_set_password'
        header = _('Set Password')
        action_button_text = _('Set password')
        back_url_name = 'account'

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def clean(self) -> dict[str, Any] | None:  # noqa: D400, D415
        """
        :meta private:
        """
        if self.data:
            data = self.data.copy()  # type: ignore[attr-defined]
            data['password2'] = data.get('password1')
            self.data = data
        return super().clean()


class ChangePasswordForm(generic.Form, forms.ChangePasswordForm):  # type: ignore[misc]
    oldpassword = fields.PasswordField(
        required=True, label=_('Current password'), autocomplete='current-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )
    password1 = fields.PasswordField(
        required=True, label=_('New password'), autocomplete='new-password',
        min_length=settings.AUTH_MIN_PASSWORD_LENGTH,  # type: ignore[misc]
        max_length=4096,
    )

    class Meta(generic.FormMeta):
        id = 'change_password'
        action_button_text = _('Change password')
        header = _('Change Password')
        action_url_name = 'account_change_password'
        back_url_name = 'account'

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
        set_form_field_order(self, ['oldpassword', 'password1'])

    def clean(self) -> dict[str, Any] | None:  # noqa: D400, D415
        """
        :meta private:
        """
        if self.data:
            data = self.data.copy()  # type: ignore[attr-defined]
            data['password2'] = data.get('password1')
            self.data = data
        return super().clean()
