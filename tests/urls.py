from __future__ import absolute_import

from django.conf.urls import url
from django.http import Http404, HttpResponse


def test_view(request):
    if request.method != 'GET':
        raise Http404()
    return HttpResponse("Test view")


def test_view_http401(request):
    return HttpResponse('Unauthorized', status=401)


def test_view_that_deletes_is_enabled(request):
    if hasattr(request, '_cors_enabled'):
        del request._cors_enabled
    return HttpResponse()


urlpatterns = [
    url(r'^$', test_view),
    url(r'^foo/$', test_view),
    url(r'^test-401/$', test_view_http401),
    url(r'^delete-is-enabled/$', test_view_that_deletes_is_enabled),
]
