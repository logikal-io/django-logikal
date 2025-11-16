from enum import Enum

from django.db.models import Case, TextChoices, Value, When
from django.db.models.expressions import Expression


class OrderedTextChoices(TextChoices):  # pylint: disable=too-many-ancestors
    @classmethod
    def order(cls, field_name: str) -> Expression:
        return Case(*(
            When(**{field_name: attribute.label}, then=Value(index))
            for index, (name, attribute) in enumerate(cls.__dict__.items())
            if isinstance(attribute, Enum)
        ))
