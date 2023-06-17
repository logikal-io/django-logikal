from django.contrib.auth.models import AbstractUser

SITE = {'domain': 'logikal.io', 'name': 'logikal.io'}


class User(AbstractUser):
    """
    Model representing users.
    """
