from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    Represents an abstract base model.
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HistorizedBaseModel(BaseModel):
    """
    Represents a historized abstract base model.
    """
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Represents an abstract base user.
    """
    email = models.EmailField(_('email'), unique=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    name = models.CharField(_('name'), max_length=300, null=True, blank=True)
    nickname = models.CharField(_('nickname'), max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm: Any, obj: Any = None):
        return True

    def has_module_perms(self, app_label: Any):
        return True

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.nickname

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
