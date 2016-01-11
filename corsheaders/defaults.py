from django.conf import settings

default_headers = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'user-agent',
    'accept-encoding',
)

CORS_ALLOW_HEADERS = getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

default_methods = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
)
CORS_ALLOW_METHODS = getattr(settings, 'CORS_ALLOW_METHODS', default_methods)

CORS_ALLOW_CREDENTIALS = getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)

CORS_PREFLIGHT_MAX_AGE = getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', 86400)

CORS_ORIGIN_ALLOW_ALL = getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', False)

CORS_ORIGIN_WHITELIST = getattr(settings, 'CORS_ORIGIN_WHITELIST', ())

CORS_ORIGIN_REGEX_WHITELIST = getattr(
    settings,
    'CORS_ORIGIN_REGEX_WHITELIST',
    ())

CORS_EXPOSE_HEADERS = getattr(settings, 'CORS_EXPOSE_HEADERS', ())

CORS_URLS_REGEX = getattr(settings, 'CORS_URLS_REGEX', '^.*$')

CORS_MODEL = getattr(settings, 'CORS_MODEL', None)

CORS_REPLACE_HTTPS_REFERER = getattr(
    settings,
    'CORS_REPLACE_HTTPS_REFERER',
    False)
CORS_URLS_ALLOW_ALL_REGEX = getattr(settings, 'CORS_URLS_ALLOW_ALL_REGEX', ())
