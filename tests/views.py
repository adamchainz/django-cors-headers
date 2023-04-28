from __future__ import annotations

from http import HTTPStatus

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    return HttpResponse("Index")


async def async_(request):
    return HttpResponse("Asynchronous")


def unauthorized(request):
    return HttpResponse("Unauthorized", status=HTTPStatus.UNAUTHORIZED)


def delete_enabled_attribute(request):
    del request._cors_enabled
    return HttpResponse()
