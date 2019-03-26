from __future__ import absolute_import

from django.conf import settings

from .defaults import default_headers, default_methods  # Kept here for backwards compatibility

class _Setting(object):
    def __init__(self,key,default):
        self.key = key
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(settings,self.key, self.default)


class Settings(object):
    """
    Shadow Django's settings with a little logic
    """

    CORS_ALLOW_HEADERS = _Setting('CORS_ALLOW_HEADERS', default_headers)

    CORS_ALLOW_METHODS = _Setting('CORS_ALLOW_METHODS', default_methods)

    CORS_ALLOW_CREDENTIALS  = _Setting('CORS_ALLOW_CREDENTIALS', False)

    CORS_PREFLIGHT_MAX_AGE  = _Setting('CORS_PREFLIGHT_MAX_AGE', 86400)

    CORS_ORIGIN_ALLOW_ALL  = _Setting('CORS_ORIGIN_ALLOW_ALL', False)

    CORS_ORIGIN_WHITELIST = _Setting('CORS_ORIGIN_WHITELIST', ())

    CORS_ORIGIN_REGEX_WHITELIST = _Setting('CORS_ORIGIN_REGEX_WHITELIST', ())

    CORS_EXPOSE_HEADERS = _Setting('CORS_EXPOSE_HEADERS', ())

    CORS_URLS_REGEX = _Setting('CORS_URLS_REGEX', r'^.*$')

    CORS_MODEL = _Setting('CORS_MODEL', None)

    CORS_REPLACE_HTTPS_REFERER = _Setting('CORS_REPLACE_HTTPS_REFERER', False)


conf = Settings()
