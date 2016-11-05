from django.conf.urls import url
from django.http import Http404, HttpResponse


def test_view(request):
    if request.method != 'GET':
        raise Http404()
    return HttpResponse("Test view")


def test_view_http401(request):
    return HttpResponse('Unauthorized', status=401)


urlpatterns = [
    url(r'^$', test_view, name='test-view'),
    url(r'^test-401/$', test_view_http401),
]
