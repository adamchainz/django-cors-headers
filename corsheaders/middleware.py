from django import http
from urlparse import urlparse

from corsheaders import defaults as settings


class CorsMiddleware(object):

    def process_request(self, request):
        '''
            If CORS preflight header, then create an empty body response (200 OK) and return it

            Django won't bother calling any other request view/exception middleware along with
            the requested view; it will call any response middlewares
        '''
        if request.method == 'OPTIONS' and request.META.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD'):
            response = http.HttpResponse()
            return response
        return None

    def process_response(self, request, response):
        '''
            Add the respective CORS headers
        '''
        origin = request.META.get('HTTP_ORIGIN')
        if origin:
            # todo: check hostname from db instead
            url = urlparse(origin)

            if not settings.CORS_ORIGIN_ALLOW_ALL and url.hostname not in settings.CORS_ORIGIN_WHITELIST:
                return response

            response['Access-Control-Allow-Origin'] = "*" if settings.CORS_ORIGIN_ALLOW_ALL else origin

            if settings.CORS_ALLOW_CREDENTIALS:
                response['Access-Control-Allow-Credentials'] = 'true'

            if request.method == 'OPTIONS':
                response['Access-Control-Allow-Headers'] = ', '.join(settings.CORS_ALLOW_HEADERS)
                response['Access-Control-Allow-Methods'] = ', '.join(settings.CORS_ALLOW_METHODS)
                if settings.CORS_PREFLIGHT_MAX_AGE:
                    response['Access-Control-Max-Age'] = settings.CORS_PREFLIGHT_MAX_AGE

        return response
