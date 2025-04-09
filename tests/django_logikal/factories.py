from typing import Any

import robots
from django.contrib.sites.models import Site
from factory.declarations import LazyFunction
from factory.django import DjangoModelFactory, Password
from factory.faker import Faker
from factory.helpers import post_generation
from faker import Faker as FakerFactory

from tests.dynamic_site.models import Project, User

faker = FakerFactory()


class UserFactory(DjangoModelFactory[User]):
    username = 'user'
    password = Password('local')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')

    class Meta:
        model = User


class StaffUserFactory(UserFactory):
    username = 'staff_user'
    is_staff = True


class SuperUserFactory(StaffUserFactory):
    username = 'super_user'
    is_superuser = True


class RobotsUrlFactory(DjangoModelFactory[robots.models.Url]):
    class Meta:
        model = robots.models.Url


class RobotsRuleFactory(DjangoModelFactory[robots.models.Rule]):
    robot = '*'

    class Meta:
        model = robots.models.Rule
        skip_postgeneration_save = True

    @post_generation  # type: ignore[misc]
    def disallowed(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: list[robots.models.Url],
        **_kwargs: Any,
    ) -> None:
        for url in extracted:
            self.disallowed.add(url)

    @post_generation  # type: ignore[misc]
    def sites(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: list[Site],
        **_kwargs: Any,
    ) -> None:
        for site in extracted:
            self.sites.add(site)


class ProjectFactory(DjangoModelFactory[Project]):
    id = Faker('uuid4')
    name = LazyFunction(lambda: faker.bs().title())

    class Meta:
        model = Project
