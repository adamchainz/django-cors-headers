from django.conf.urls import url
from django.http import HttpResponse


def test_view(request):
    return HttpResponse("Test view")


def test_view_http401(request):
    return HttpResponse('Unauthorized', status=401)


urlpatterns = [
    url(r'^test-view/$', test_view, name='test-view'),
    url(r'^test-view-http401/$', test_view_http401, name='test-view-http401'),
]
