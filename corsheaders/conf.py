from __future__ import absolute_import

from django.conf import settings

from corsheaders.defaults import default_headers, default_methods  # Kept here for backwards compatibility


class Settings(object):
    """
    Shadow Django's settings with a little logic
    """

    @property
    def CORS_ALLOW_HEADERS(self):
        return getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

    @property
    def CORS_ALLOW_METHODS(self):
        return getattr(settings, 'CORS_ALLOW_METHODS', default_methods)

    @property
    def CORS_ALLOW_CREDENTIALS(self):
        return getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)

    @property
    def CORS_PREFLIGHT_MAX_AGE(self):
        return getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', 86400)

    @property
    def CORS_ORIGIN_ALLOW_ALL(self):
        return getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', False)

    @property
    def CORS_ORIGIN_WHITELIST(self):
        return getattr(settings, 'CORS_ORIGIN_WHITELIST', ())

    @property
    def CORS_ORIGIN_REGEX_WHITELIST(self):
        return getattr(settings, 'CORS_ORIGIN_REGEX_WHITELIST', ())

    @property
    def CORS_EXPOSE_HEADERS(self):
        return getattr(settings, 'CORS_EXPOSE_HEADERS', ())

    @property
    def CORS_URLS_REGEX(self):
        return getattr(settings, 'CORS_URLS_REGEX', r'^.*$')

    @property
    def CORS_REPLACE_HTTPS_REFERER(self):
        return getattr(settings, 'CORS_REPLACE_HTTPS_REFERER', False)


conf = Settings()
