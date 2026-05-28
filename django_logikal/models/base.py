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
    is_active = models.BooleanField(_('active'), default=True)
    name = models.CharField(_('name'), max_length=300, null=True, blank=True)
    nickname = models.CharField(_('nickname'), max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> bool:
        return self.is_admin

    def get_full_name(self) -> str | None:
        return self.name

    def get_short_name(self) -> str | None:
        return self.nickname

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
