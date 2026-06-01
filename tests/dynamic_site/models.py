# pylint: disable=too-many-ancestors
from django.db.models import CharField, DateField, F
from django.db.models.functions import Lower
from rest_framework import serializers, viewsets

from django_logikal.models.base import BaseModel, BaseUser, HistorizedBaseModel
from django_logikal.models.text_choices import OrderedTextChoices

SITE = {'domain': 'logikal.io', 'name': 'logikal.io'}


class User(HistorizedBaseModel, BaseUser):
    """
    Model representing users.
    """


class Status(OrderedTextChoices):
    PLANNING = ('planning', 'planning')
    ACTIVE = ('active', 'active')
    COMPLETED = ('completed', 'completed')
    CANCELED = ('canceled', 'canceled')


class Project(BaseModel):
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
