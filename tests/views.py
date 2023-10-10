from __future__ import annotations

from http import HTTPStatus

from django.http import HttpResponse
from django.views.decorators.http import require_GET

from corsheaders.conf import Settings
from corsheaders.decorators import cors


@require_GET
def index(request):
    return HttpResponse("Index")


async def async_(request):
    return HttpResponse("Asynchronous")


@cors
def decorated(request, slug):
    return HttpResponse(f"Decorated: {slug}")


@cors(conf=Settings(CORS_ALLOWED_ORIGINS=["https://example.com"]))
def decorated_with_conf(request, slug):
    return HttpResponse(f"Decorated (with conf): {slug}")


@cors
async def async_decorated(request, slug):
    return HttpResponse(f"Async Decorated: {slug}")


@cors(conf=Settings(CORS_ALLOWED_ORIGINS=["https://example.com"]))
async def async_decorated_with_conf(request, slug):
    return HttpResponse(f"Async Decorated (with conf): {slug}")


def unauthorized(request):
    return HttpResponse("Unauthorized", status=HTTPStatus.UNAUTHORIZED)


def delete_enabled_attribute(request):
    del request._cors_enabled
    return HttpResponse()
