from typing import Any, List

import robots
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from factory import Faker, LazyFunction, post_generation
from factory.django import DjangoModelFactory
from faker import Faker as FakerFactory

from tests.dynamic_site.models import Project, User

faker = FakerFactory()


class UserFactory(DjangoModelFactory):  # type: ignore[misc]
    username = 'user'
    password = LazyFunction(lambda: make_password('local'))  # nosec: used for testing
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


class RobotsUrlFactory(DjangoModelFactory):  # type: ignore[misc]
    class Meta:
        model = robots.models.Url


class RobotsRuleFactory(DjangoModelFactory):  # type: ignore[misc]
    robot = '*'

    class Meta:
        model = robots.models.Rule
        skip_postgeneration_save = True

    @post_generation  # type: ignore[misc]
    def disallowed(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: List[robots.models.Url],
        **_kwargs: Any,
    ) -> None:
        for url in extracted:
            self.disallowed.add(url)

    @post_generation  # type: ignore[misc]
    def sites(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: List[Site],
        **_kwargs: Any,
    ) -> None:
        for site in extracted:
            self.sites.add(site)


class ProjectFactory(DjangoModelFactory):  # type: ignore[misc]
    name = LazyFunction(lambda: faker.bs().title())

    class Meta:
        model = Project
