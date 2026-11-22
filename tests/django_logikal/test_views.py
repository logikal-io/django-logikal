import re
from datetime import date
from typing import cast

from django import forms
from django.template.response import TemplateResponse
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
    template_name = 'dynamic_site/models.html.j'
    success_url = '/updated/'


@mark.django_db
def test_htmx_update_get(rf: RequestFactory) -> None:
    project = cast(
        Project,
        ProjectFactory(name='original', status=Status.ACTIVE, start_date=date(2026, 1, 1)),
    )

    # Send a get request for the project
    request = rf.get(f'/projects/{project.pk}/')
    request.htmx = False  # type: ignore[attr-defined]

    response = ProjectUpdateView.as_view()(request, pk=project.pk)

    # Check that the template has been rendered with the appropriate context
    assert isinstance(response, TemplateResponse)
    assert response.status_code == 200
    assert response.context_data is not None
    assert response.context_data['object'] == project
    assert response.context_data['form'].initial['name'] == 'original'


@mark.django_db
def test_htmx_update_submission(rf: RequestFactory) -> None:
    project = cast(
        Project,
        ProjectFactory(name='original', status=Status.ACTIVE, start_date=date(2026, 1, 1)),
    )

    # Send a value for update
    request = rf.post(f'/projects/{project.pk}/', {'name': 'renamed'})
    request.htmx = False  # type: ignore[attr-defined]
    response = ProjectUpdateView.as_view()(request, pk=project.pk)

    # Check that the new value has been saved and a redirect has been issued
    project.refresh_from_db()
    assert project.name == 'renamed'
    assert response.status_code == 302
    assert response.headers['Location'] == ProjectUpdateView.success_url


@mark.django_db
@mark.parametrize('status', [Status.PLANNING, Status.ACTIVE])
def test_htmx_update_validation(rf: RequestFactory, status: Status) -> None:
    project = cast(
        Project,
        ProjectFactory(name='original', status=status, start_date=date(2026, 1, 1)),
    )

    # Send a value with htmx for validation
    request = rf.post(f'/projects/{project.pk}/', {'name': 'renamed'})
    request.htmx = True  # type: ignore[attr-defined]
    response = ProjectUpdateView.as_view()(request, pk=project.pk)
    response_content = response.content.decode()  # type: ignore[attr-defined]

    # Check that the new value has not been saved
    project.refresh_from_db()
    assert project.name == 'original'

    # Check the validation result
    assert response.status_code == 200
    if status == Status.PLANNING:
        assert '<li>Only active projects can be renamed.</li>' in response_content
    else:
        assert re.search(r'<ul class="errors">\s*</ul>', response_content)  # no errors
