import re

from django import http
from django.apps import apps

from .conf import corsheaders_settings
from .signals import check_request_enabled

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object

ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsPostCsrfMiddleware(MiddlewareMixin):

    def _https_referer_replace_reverse(self, request):
        """
        Put the HTTP_REFERER back to its original value and delete the
        temporary storage
        """
        if corsheaders_settings.CORS_REPLACE_HTTPS_REFERER and 'ORIGINAL_HTTP_REFERER' in request.META:
            http_referer = request.META['ORIGINAL_HTTP_REFERER']
            request.META['HTTP_REFERER'] = http_referer
            del request.META['ORIGINAL_HTTP_REFERER']

    def process_request(self, request):
        self._https_referer_replace_reverse(request)
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        self._https_referer_replace_reverse(request)
        return None


class CorsMiddleware(MiddlewareMixin):

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
            if (
                not corsheaders_settings.CORS_ORIGIN_ALLOW_ALL and
                self.origin_not_found_in_white_lists(origin, url)
            ):
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
        if self.is_enabled(request) and corsheaders_settings.CORS_REPLACE_HTTPS_REFERER:
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
        if self.is_enabled(request) and corsheaders_settings.CORS_REPLACE_HTTPS_REFERER:
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

            if corsheaders_settings.CORS_MODEL is not None:
                model = apps.get_model(*corsheaders_settings.CORS_MODEL.split('.'))
                if model.objects.filter(cors=url.netloc).exists():
                    response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

            if (
                not corsheaders_settings.CORS_ORIGIN_ALLOW_ALL and
                self.origin_not_found_in_white_lists(origin, url) and
                not self.check_signal(request)
            ):
                return response

            if corsheaders_settings.CORS_ORIGIN_ALLOW_ALL and not corsheaders_settings.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
            else:
                response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

            if len(corsheaders_settings.CORS_EXPOSE_HEADERS):
                response[ACCESS_CONTROL_EXPOSE_HEADERS] = ', '.join(corsheaders_settings.CORS_EXPOSE_HEADERS)

            if corsheaders_settings.CORS_ALLOW_CREDENTIALS:
                response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

            if request.method == 'OPTIONS':
                response[ACCESS_CONTROL_ALLOW_HEADERS] = ', '.join(corsheaders_settings.CORS_ALLOW_HEADERS)
                response[ACCESS_CONTROL_ALLOW_METHODS] = ', '.join(corsheaders_settings.CORS_ALLOW_METHODS)
                if corsheaders_settings.CORS_PREFLIGHT_MAX_AGE:
                    response[ACCESS_CONTROL_MAX_AGE] = corsheaders_settings.CORS_PREFLIGHT_MAX_AGE

        return response

    def origin_not_found_in_white_lists(self, origin, url):
        return (
            url.netloc not in corsheaders_settings.CORS_ORIGIN_WHITELIST and
            not self.regex_domain_match(origin)
        )

    def regex_domain_match(self, origin):
        for domain_pattern in corsheaders_settings.CORS_ORIGIN_REGEX_WHITELIST:
            if re.match(domain_pattern, origin):
                return origin

    def is_enabled(self, request):
        return (
            re.match(corsheaders_settings.CORS_URLS_REGEX, request.path) or
            self.check_signal(request)
        )

    def check_signal(self, request):
        signal_responses = check_request_enabled.send(
            sender=None,
            request=request,
        )
        return any(
            return_value for
            function, return_value in signal_responses
        )
