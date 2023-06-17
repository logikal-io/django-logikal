from typing import Dict, List, Union

from django.contrib.messages import get_messages
from django.contrib.messages.storage.base import BaseStorage, Message
from django.http.request import HttpRequest


def add_messages(request: HttpRequest) -> Dict[str, Union[List[Message], BaseStorage]]:
    return {'messages': get_messages(request=request)}
