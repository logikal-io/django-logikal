from pathlib import Path
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from django_logikal.email import Email
from django_logikal.views import PublicViewMixin
from tests.dynamic_site.models import Project


class ListProjects(PublicViewMixin, ListView[Project]):
    model = Project
    template_name = 'dynamic_site/models.html.j'
    context_object_name = 'projects'


class EmailView(PublicViewMixin, TemplateView):
    template_name = 'dynamic_site/email.html.j'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        email = Email(template='dynamic_site/email/test_email.html.j')
        email.attach('inline_attachment.txt', content='Inline Attachment')
        email.attach_file(Path(__file__).parent / 'attachment.txt')
        email.send(sender='testing@django-logikal.org', to=['success@simulator.amazonses.com'])
        return super().get(request, *args, **kwargs)
