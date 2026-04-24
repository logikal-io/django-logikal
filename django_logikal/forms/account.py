from typing import Any

import allauth


class SetPasswordForm(allauth.account.forms.SetPasswordForm):
    def clean(self) -> dict[str, Any] | None:
        if self.data:
            data = self.data.copy()
            data['password2'] = data.get('password1')
            self.data = data
        return super().clean()


class ChangePasswordForm(allauth.account.forms.ChangePasswordForm):
    def clean(self) -> dict[str, Any] | None:
        if self.data:
            data = self.data.copy()
            data['password2'] = data.get('password1')
            self.data = data
        return super().clean()
