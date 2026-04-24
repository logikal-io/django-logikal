from typing import Any

import robots
from django.contrib.sites.models import Site
from factory.declarations import LazyAttribute, LazyFunction
from factory.django import DjangoModelFactory, Password
from factory.faker import Faker
from factory.helpers import post_generation
from faker import Faker as FakerFactory

from tests.dynamic_site.models import SITE, Project, User

DOMAIN = 'django-logikal.org'
faker = FakerFactory()


def site_factory() -> Site:  # note that the site is cleared for each test by pytest-django
    return Site.objects.update_or_create(id=1, defaults=SITE)[0]


class UserFactory(DjangoModelFactory[User]):
    email = LazyAttribute(lambda obj: f'{obj.name.replace(' ', '.').lower()}@{DOMAIN}')
    password = Password('local')
    name = Faker('name')
    nickname = LazyAttribute(lambda obj: obj.name.split(' ')[0])

    class Meta:
        model = User


class AdminUserFactory(UserFactory):
    email = f'admin-user@{DOMAIN}'
    is_admin = True


class SuperUserFactory(AdminUserFactory):
    email = f'super-user@{DOMAIN}'
    is_superuser = True


class RobotsUrlFactory(DjangoModelFactory[robots.models.Url]):
    class Meta:
        model = robots.models.Url


class RobotsRuleFactory(DjangoModelFactory[robots.models.Rule]):
    robot = '*'

    class Meta:
        model = robots.models.Rule
        skip_postgeneration_save = True

    @post_generation  # type: ignore[untyped-decorator]
    def disallowed(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: list[robots.models.Url],
        **_kwargs: Any,
    ) -> None:
        for url in extracted:
            self.disallowed.add(url)

    @post_generation  # type: ignore[untyped-decorator]
    def sites(
        self,
        create: bool,  # pylint: disable=unused-argument
        extracted: list[Site],
        **_kwargs: Any,
    ) -> None:
        for site in extracted:
            self.sites.add(site)


class ProjectFactory(DjangoModelFactory[Project]):
    name = LazyFunction(lambda: faker.bs().title())

    class Meta:
        model = Project
