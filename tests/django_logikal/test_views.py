# pylint: disable=too-many-ancestors
import re
from datetime import date
from typing import cast

from django import forms
from django.test import RequestFactory
from pytest import mark

from django_logikal.forms.generic import Form, FormMeta
from django_logikal.views.generic import HTMXUpdateView
from tests.django_logikal.factories import ProjectFactory
from tests.dynamic_site.models import Project, Status


class ProjectForm(Form, forms.ModelForm[Project]):
    class Meta(FormMeta):
        id = 'project'
        model = Project
        fields = ['name']

    def clean_name(self) -> str:
        if self.instance.status != Status.ACTIVE:
            raise forms.ValidationError('Only active projects can be renamed.')
        return self.cleaned_data['name']  # type: ignore[no-any-return]


class ProjectUpdateView(HTMXUpdateView[Project, ProjectForm]):
    model = Project
    form_class = ProjectForm


@mark.django_db
@mark.parametrize('status', [Status.PLANNING, Status.ACTIVE])
def test_htmx_update_validation(rf: RequestFactory, status: Status) -> None:
    project = cast(
        Project, ProjectFactory(name='original', status=status, start_date=date(2026, 1, 1)),
    )

    # Send a value with htmx for validation
    request = rf.post(f'/projects/{project.pk}/', {'name': 'renamed'})
    request.htmx = True  # type: ignore[attr-defined]
    response = ProjectUpdateView.as_view()(request, pk=project.pk)
    response_content = response.content.decode()

    # Check the validation result
    assert response.status_code == 200
    if status == Status.PLANNING:
        assert '<li>Only active projects can be renamed.</li>' in response_content
    else:
        assert re.search(r'<ul class="errors">\s*</ul>', response_content)  # no errors

    # Check that the new value has not been saved
    project.refresh_from_db()
    assert project.name == 'original'
