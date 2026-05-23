from typing import Any

from django.forms import widgets


class EmailInput(widgets.Input):
    template_name = 'django_logikal/forms/widgets/input.html.j'
    input_type = 'email'


class PasswordInput(widgets.Input):
    template_name = 'django_logikal/forms/widgets/password.html.j'
    input_type = 'password'
    icon_show = 'django_logikal/icons/password_show.svg'
    icon_hide = 'django_logikal/icons/password_hide.svg'

    def get_context(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context(*args, **kwargs)
        context['widget']['icon_show'] = self.icon_show
        context['widget']['icon_hide'] = self.icon_hide
        return context
