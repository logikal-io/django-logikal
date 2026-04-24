from enum import Enum

from django.db import models


class OrderedTextChoices(models.TextChoices):
    @classmethod
    def order(cls, field_name: str) -> models.expressions.Expression:
        return models.Case(*(
            models.When(**{field_name: attribute.label}, then=models.Value(index))
            for index, (name, attribute) in enumerate(cls.__dict__.items())
            if isinstance(attribute, Enum)
        ))
