# pylint: disable=too-many-ancestors
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, DateField, F, UUIDField
from django.db.models.functions import Lower
from rest_framework import serializers, viewsets
from simple_history.models import HistoricalRecords

from django_logikal.models import OrderedTextChoices

SITE = {'domain': 'logikal.io', 'name': 'logikal.io'}


class User(AbstractUser):
    """
    Model representing users.
    """
    history = HistoricalRecords()


class Status(OrderedTextChoices):
    PLANNING = ('planning', 'planning')
    ACTIVE = ('active', 'active')
    COMPLETED = ('completed', 'completed')
    CANCELED = ('canceled', 'canceled')


class Project(models.Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = CharField(max_length=150)
    start_date = DateField()
    end_date = DateField(null=True, blank=True)
    status = CharField(choices=Status.choices, default=Status.PLANNING)

    class Meta:
        ordering = [
            Status.order('status'), Lower('name'),
            'start_date', F('end_date').asc(nulls_last=True),
        ]


class ProjectSerializer(serializers.HyperlinkedModelSerializer[Project]):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectViewSet(viewsets.ModelViewSet[Project]):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
