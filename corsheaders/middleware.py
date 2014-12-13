import re

from django import http
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from corsheaders import defaults as settings
from django.db.models.loading import get_model


ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsMiddleware(object):

    def process_request(self, request):
        """
        If CORS preflight header, then create an
        empty body response (200 OK) and return it

        Django won't bother calling any other request
        view/exception middleware along with the requested view;
        it will call any response middlewares
        """
        if (self.is_enabled(request) and
                request.method == 'OPTIONS' and
                "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META):
            response = http.HttpResponse()
            return response
        return None

    def process_response(self, request, response):
        """
        Add the respective CORS headers
        """
        origin = request.META.get('HTTP_ORIGIN')
        if self.is_enabled(request) and origin:
            # todo: check hostname from db instead
            url = urlparse(origin)

            if settings.CORS_MODEL is not None:
                model = get_model(*settings.CORS_MODEL.split('.'))
                if model.objects.filter(cors=url.netloc).exists():
                    response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

            if (not settings.CORS_ORIGIN_ALLOW_ALL and
                    self.origin_not_found_in_white_lists(origin, url)):
                return response

            response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*" if (
                settings.CORS_ORIGIN_ALLOW_ALL and
                not settings.CORS_ALLOW_CREDENTIALS) else origin

            if len(settings.CORS_EXPOSE_HEADERS):
                response[ACCESS_CONTROL_EXPOSE_HEADERS] = ', '.join(
                    settings.CORS_EXPOSE_HEADERS)

            if settings.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

            if request.method == 'OPTIONS':
                response[ACCESS_CONTROL_ALLOW_HEADERS] = ', '.join(
                    settings.CORS_ALLOW_HEADERS)
                response[ACCESS_CONTROL_ALLOW_METHODS] = ', '.join(
                    settings.CORS_ALLOW_METHODS)
                if settings.CORS_PREFLIGHT_MAX_AGE:
                    response[ACCESS_CONTROL_MAX_AGE] = settings.CORS_PREFLIGHT_MAX_AGE

        return response

    def origin_not_found_in_white_lists(self, origin, url):
        return (url.netloc not in settings.CORS_ORIGIN_WHITELIST and
                not self.regex_domain_match(origin))

    def regex_domain_match(self, origin):
        for domain_pattern in settings.CORS_ORIGIN_REGEX_WHITELIST:
            if re.match(domain_pattern, origin):
                return origin

    def is_enabled(self, request):
        return re.match(settings.CORS_URLS_REGEX, request.path)
