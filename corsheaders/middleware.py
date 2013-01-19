from urlparse import urlparse

from corsheaders import defaults as settings


class CorsMiddleware(object):
    def process_response(self, request, response):
        origin = request.META.get('HTTP_ORIGIN')
        if origin:
            # todo: check hostname from db instead
            url = urlparse(origin)

            if not settings.CORS_ORIGIN_ALLOW_ALL and url.hostname not in settings.CORS_ORIGIN_WHITELIST:
                return response

            response['Access-Control-Allow-Origin'] = "*" if settings.CORS_ORIGIN_ALLOW_ALL else origin

            if request.method == 'OPTIONS':
                response['Access-Control-Allow-Headers'] = ', '.join(settings.CORS_ALLOW_HEADERS)
                response['Access-Control-Allow-Methods'] = ', '.join(settings.CORS_ALLOW_METHODS)
                if settings.CORS_ALLOW_CREDENTIALS:
                    response['Access-Control-Allow-Credentials'] = 'true'
                if settings.CORS_PREFLIGHT_MAX_AGE:
                    response['Access-Control-Max-Age'] = settings.CORS_PREFLIGHT_MAX_AGE

        return response
