from pytest_factoryboy import register

from tests.django_logikal import factories

register(factories.UserFactory)
register(factories.AdminUserFactory, _name='admin_user')
register(factories.SuperUserFactory, _name='super_user')
