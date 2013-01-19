from django.conf import settings
from urlparse import urlparse

allow_headers = getattr(settings, 'CORS_ALLOW_HEADERS', ('x-requested-with',
                                                         'content-type',
                                                         'accept',
                                                         'origin'))

allow_methods = getattr(settings, 'CORS_ALLOW_METHODS', ('GET',
                                                         'POST',
                                                         'PUT',
                                                         'PATCH',
                                                         'DELETE',
                                                         'OPTIONS'))
allow_credentials = getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)
max_age = getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', None)

origin_whitelist = getattr(settings, 'CORS_ORIGIN_WHITELIST', None)

class CorsMiddleware(object):

    def process_response(self, request, response):
        origin = request.META.get('HTTP_ORIGIN')
        method = request.method
        if origin:
            # todo: check hostname from db instead
            url = urlparse(origin)

            if origin_whitelist and url.hostname not in origin_whitelist:
                return response # return response without CORS headers

            response['Access-Control-Allow-Origin'] = "*" if not origin_whitelist else origin

            if request.method == 'OPTIONS':
                response['Access-Control-Allow-Headers'] = ', '.join(allow_headers)
                response['Access-Control-Allow-Methods'] = ', '.join(allow_methods)
                if allow_credentials:
                    response['Access-Control-Allow-Credentials'] = 'true'
                if max_age:
                    response['Access-Control-Max-Age'] = max_age

        return response
