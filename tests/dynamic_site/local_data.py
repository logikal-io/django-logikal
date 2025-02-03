# mypy: disable-error-code="no-untyped-call, attr-defined"
from datetime import date

from django_logikal.local_data import LocalData, SkipInsert
from tests.django_logikal import factories
from tests.dynamic_site.models import Status


class UserData(LocalData):
    @staticmethod
    def insert() -> None:
        factories.UserFactory()
        factories.StaffUserFactory()
        factories.SuperUserFactory()


class ProjectData(LocalData):
    @staticmethod
    def insert() -> None:
        project_1 = factories.ProjectFactory(
            start_date=date(2023, 2, 1), end_date=date(2023, 2, 10),
            status=Status.PLANNING,
        )
        project_2 = factories.ProjectFactory(
            start_date=date(2023, 1, 1), end_date=date(2023, 1, 20),
            status=Status.COMPLETED,
        )
        factories.ProjectFactory(  # same name, different status
            name=project_1.name, start_date=project_1.start_date, end_date=project_1.end_date,
            status=Status.COMPLETED,
        )
        factories.ProjectFactory(  # same name and start date, no end date
            name=project_2.name, start_date=project_2.start_date,
            status=Status.COMPLETED,
        )


class SkippedData(LocalData):
    @staticmethod
    def insert() -> None:
        raise SkipInsert('Intentionally skipped')  # pragma: no cover
