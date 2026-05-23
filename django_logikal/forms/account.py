from django.utils.translation import gettext_lazy as _

from django_logikal.forms import fields
from django_logikal.forms.generic import Form, FormMeta


class AuthForm(Form):
    email = fields.EmailField(
        required=True, label=_('Email address'), placeholder=_('email@example.com'),
        autocomplete='username', spellcheck=False,
    )

    class Meta(FormMeta):
        id = 'auth'
        action_url_name = 'account_auth'
        action_button_text = _('Next')
