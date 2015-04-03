import re

from django import http
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from corsheaders import defaults as settings


ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsPostCsrfMiddleware(object):

    def _https_referer_replace_reverse(self, request):
        """
        Put the HTTP_REFERER back to its original value and delete the
        temporary storage
        """
        if (settings.CORS_REPLACE_HTTPS_REFERER and
                'ORIGINAL_HTTP_REFERER' in request.META):
            http_referer = request.META['ORIGINAL_HTTP_REFERER']
            request.META['HTTP_REFERER'] = http_referer
            del request.META['ORIGINAL_HTTP_REFERER']

    def process_request(self, request):
        self._https_referer_replace_reverse(request)
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        self._https_referer_replace_reverse(request)
        return None


class CorsMiddleware(object):

    def _https_referer_replace(self, request):
        """
        When https is enabled, django CSRF checking includes referer checking
        which breaks when using CORS. This function updates the HTTP_REFERER
        header to make sure it matches HTTP_HOST, provided that our cors logic
        succeeds
        """
        origin = request.META.get('HTTP_ORIGIN')

        if (request.is_secure() and origin and
                'ORIGINAL_HTTP_REFERER' not in request.META):
            url = urlparse(origin)
            if (not settings.CORS_ORIGIN_ALLOW_ALL and
                    self.origin_not_found_in_white_lists(origin, url)):
                return

            try:
                http_referer = request.META['HTTP_REFERER']
                http_host = "https://%s/" % request.META['HTTP_HOST']
                request.META = request.META.copy()
                request.META['ORIGINAL_HTTP_REFERER'] = http_referer
                request.META['HTTP_REFERER'] = http_host
            except KeyError:
                pass

    def process_request(self, request):
        """
        If CORS preflight header, then create an
        empty body response (200 OK) and return it

        Django won't bother calling any other request
        view/exception middleware along with the requested view;
        it will call any response middlewares
        """
        if self.is_enabled(request) and settings.CORS_REPLACE_HTTPS_REFERER:
            self._https_referer_replace(request)

        if (self.is_enabled(request) and
                request.method == 'OPTIONS' and
                "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META):
            response = http.HttpResponse()
            return response
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Do the referer replacement here as well
        """
        if self.is_enabled(request) and settings.CORS_REPLACE_HTTPS_REFERER:
            self._https_referer_replace(request)
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
                    response[ACCESS_CONTROL_MAX_AGE] = \
                        settings.CORS_PREFLIGHT_MAX_AGE

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
