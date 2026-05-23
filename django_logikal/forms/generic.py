from typing import Any, Self

from django import forms
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise
from logikal_utils.imports import installed

from django_logikal.templates.functions import url


class ErrorList(forms.utils.ErrorList):
    """
    Improved error list class.
    """
    template_name = 'django_logikal/forms/errors/list/default.html.j'

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.error_class = ' '.join(
            item if item != 'errorlist' else 'errors'
            for item in self.error_class.split()
        )


class FormRenderer(forms.renderers.BaseRenderer):
    form_template_name = 'django_logikal/forms/form.html.j'
    formset_template_name = 'django_logikal/forms/formsets/div.html.j'
    field_template_name = 'django_logikal/forms/field.html.j'

    def get_template(self, template_name: str) -> Any:
        return get_template(template_name=template_name)


class FormMeta:
    """
    Metadata class for forms.
    """
    # Form attributes
    id: str  #: The form ID to use.
    id_prefix = 'id_form'  #: The form ID prefix to use.
    action_url_name: str  #: The URL name to use for the form action.
    action_method = 'post'  #: The form action method to use.
    render_tag = True  #: Whether to render the ``<form>`` tag.

    # Element attributes
    header: StrOrPromise | None = None  #: The form header to use.
    help_text: StrOrPromise | None = None  #: The form help text to use.
    action_button_text: StrOrPromise | None = None  #: The text to use for the action button.
    back_url_name: str | None = None  #: The URL name to use for the back action.
    back_url_text: StrOrPromise = _('Back')  #: The text to use for the back button.

    # Validation attributes
    htmx_validation_trigger = 'change, keyup delay:250ms changed'  #: The htmx validation trigger.


class Form(forms.Form):
    """
    Improved parent class for forms.
    """
    default_renderer = FormRenderer()
    template_name_label = 'django_logikal/forms/label.html.j'

    Meta: FormMeta  #: The form metadata class to use.

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *args: Any,
        error_class: type[ErrorList] = ErrorList,
        label_suffix: str = '',
        render_context: dict[str, Any] | None = None,
        action_url_kwargs: dict[str, Any] | None = None,
        back_url_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        if not hasattr(self, 'Meta'):
            raise RuntimeError('The form metadata class must be specified')

        self.render_context = render_context or {}
        self.action_url_kwargs = action_url_kwargs or {}
        self.back_url_kwargs = back_url_kwargs or {}

        # Regarding type ignores see https://github.com/python/mypy/issues/6799
        super().__init__(
            *args,
            error_class=error_class,  # type: ignore[misc]
            label_suffix=label_suffix,
            **kwargs,
        )
        self.add_htmx_validation()

    def with_meta(self, **kwargs: Any) -> Self:
        """
        Return the form with the updated metadata.
        """
        for attr, value in kwargs.items():
            setattr(self.Meta, attr, value)
        return self

    def add_htmx_validation(self) -> None:
        """
        Add htmx validation data fields to all fields with an ``htmx_validate`` attribute.

        Data fields are only added when the ``htmx`` extra is installed.
        This method is automatically called during form initialization.
        """
        if not installed('django_htmx'):  # pragma: no cover, defensive line
            return
        for field_name, field in self.fields.items():
            if getattr(field, 'htmx_validate', None):
                field.widget.attrs.update({
                    'data-hx-post': url(self.Meta.action_url_name, kwargs=self.action_url_kwargs),
                    'data-hx-trigger': self.Meta.htmx_validation_trigger,
                    'data-hx-target': 'next .errors',
                    'data-hx-swap': 'outerHTML',
                    'data-hx-params': field_name,
                })

    def get_context(self) -> dict[str, Any]:
        return {**super().get_context(), **self.render_context}
