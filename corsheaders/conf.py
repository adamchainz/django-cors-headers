import six
from django.conf import settings

from .defaults import default_headers, default_methods  # Kept here for backwards compatibility
from .validators import return_type

class Settings(object):
    """
    Shadow Django's settings with a little logic
    """

    @property
    @return_type(list, tuple)
    def CORS_ALLOW_HEADERS(self):
        return getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

    @property
    @return_type(list, tuple)
    def CORS_ALLOW_METHODS(self):
        return getattr(settings, 'CORS_ALLOW_METHODS', default_methods)

    @property
    @return_type(bool)
    def CORS_ALLOW_CREDENTIALS(self):
        return getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)

    @property
    @return_type(int)
    def CORS_PREFLIGHT_MAX_AGE(self):
        return getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', 86400)

    @property
    @return_type(bool)
    def CORS_ORIGIN_ALLOW_ALL(self):
        return getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', False)

    @property
    @return_type(list, tuple)
    def CORS_ORIGIN_WHITELIST(self):
        return getattr(settings, 'CORS_ORIGIN_WHITELIST', ())

    @property
    @return_type(list, tuple)
    def CORS_ORIGIN_REGEX_WHITELIST(self):
        return getattr(settings, 'CORS_ORIGIN_REGEX_WHITELIST', ())

    @property
    @return_type(list, tuple)
    def CORS_EXPOSE_HEADERS(self):
        return getattr(settings, 'CORS_EXPOSE_HEADERS', ())

    @property
    @return_type(str)
    def CORS_URLS_REGEX(self):
        return getattr(settings, 'CORS_URLS_REGEX', r'^.*$')

    @property
    @return_type(str, type(None))
    def CORS_MODEL(self):
        return getattr(settings, 'CORS_MODEL', None)

    @property
    @return_type(bool)
    def CORS_REPLACE_HTTPS_REFERER(self):
        return getattr(settings, 'CORS_REPLACE_HTTPS_REFERER', False)

corsheaders_settings = Settings()
