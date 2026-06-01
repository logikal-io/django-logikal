from django.contrib.messages import get_messages
from django.contrib.messages.storage.base import BaseStorage, Message
from django.http import HttpRequest
from django.middleware.csp import get_nonce
from django.utils.csp import LazyNonce


def add_messages(request: HttpRequest) -> dict[str, list[Message] | BaseStorage]:
    return {'messages': get_messages(request=request)}


def add_csp_nonce(request: HttpRequest) -> dict[str, LazyNonce | None]:
    return {'csp_nonce': get_nonce(request=request)}
