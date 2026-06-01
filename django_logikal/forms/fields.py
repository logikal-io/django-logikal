from typing import Any

from django.forms import fields
from django.forms.widgets import Widget
from django_stubs_ext import StrOrPromise

from django_logikal.forms import widgets


class HTMXValidated:
    htmx_validate = True


class InputFieldMixin:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        placeholder: StrOrPromise | None = None,
        autofocus: bool | None = None,
        autocomplete: str | None = None,
        spellcheck: bool | None = None,
        read_only: bool | None = None,
        **kwargs: Any,
    ):
        attrs: dict[str, StrOrPromise | bool] = {}
        if placeholder is not None:
            attrs['placeholder'] = placeholder
        if autofocus is not None:
            attrs['autofocus'] = autofocus
        if autocomplete is not None:
            attrs['autocomplete'] = autocomplete
        if spellcheck is not None:
            attrs['spellcheck'] = str(spellcheck).lower()
        if read_only is not None:
            attrs['readonly'] = read_only

        self._extra_widget_attrs = attrs

        super().__init__(**kwargs)

    def widget_attrs(self, widget: Widget) -> dict[str, Any]:
        return {
            **self._extra_widget_attrs,
            **super().widget_attrs(widget),  # type: ignore[misc]
        }


class EmailField(HTMXValidated, InputFieldMixin, fields.EmailField):
    widget = widgets.EmailInput()


class PasswordField(HTMXValidated, InputFieldMixin, fields.CharField):
    widget = widgets.PasswordInput()

    def __init__(self, **kwargs: Any):
        kwargs.setdefault('autocomplete', 'current-password')
        kwargs.setdefault('autofocus', False)
        kwargs.setdefault('spellcheck', False)
        kwargs.setdefault('strip', False)
        super().__init__(**kwargs)
