from django.http import Http404, HttpResponse
from django.urls import path


def test_view(request):
    if request.method != "GET":
        raise Http404()
    return HttpResponse("Test view")


def test_view_http401(request):
    return HttpResponse("Unauthorized", status=401)


def test_view_that_deletes_is_enabled(request):
    if hasattr(request, "_cors_enabled"):
        del request._cors_enabled
    return HttpResponse()


urlpatterns = [
    path("", test_view),
    path("foo/", test_view),
    path("test-401/", test_view_http401),
    path("delete-is-enabled/", test_view_that_deletes_is_enabled),
]
