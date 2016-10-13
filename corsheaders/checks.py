import collections
import numbers

from django.core import checks
from .conf import corsheaders_settings

@checks.register
def check_settings(app_configs, **kwargs):

    errors = []
    if not isinstance(corsheaders_settings.CORS_ALLOW_HEADERS, collections.Sequence):
        errors.append(
            checks.Warning(
                "CORS_ALLOW_HEADERS must be sequence",
                id="django-cors-headers.W001"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ALLOW_METHODS, collections.Sequence):
        errors.append(
            checks.Warning(
                "CORS_ALLOW_METHODS must be sequence",
                id="django-cors-headers.W002"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ALLOW_CREDENTIALS, bool):
        errors.append(
            checks.Warning(
                "CORS_ALLOW_CREDENTIALS must be bool",
                id="django-cors-headers.W003"
            )
        )
    if not isinstance(corsheaders_settings.CORS_PREFLIGHT_MAX_AGE, numbers.Integral):
        errors.append(
            checks.Warning(
                "CORS_PREFLIGHT_MAX_AGE must be integer",
                id = "django-cors-headers.W004"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ORIGIN_ALLOW_ALL, bool):
        errors.append(
            checks.Warning(
                "CORS_ORIGIN_ALLOW_ALL must be bool",
                id="django-cors-headers.W005"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ORIGIN_WHITELIST, collections.Sequence):
        errors.append(
            checks.Warning(
                "CORS_ORIGIN_WHITELIST must be sequence",
                id="django-cors-headers.W006"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ORIGIN_REGEX_WHITELIST, collections.Sequence):
        errors.append(
            checks.Warning(
                "CORS_ORIGIN_REGEX_WHITELIST must be sequence",
                id="django-cors-headers.W007"
            )
        )
    if not isinstance(corsheaders_settings.CORS_EXPOSE_HEADERS, collections.Sequence):
        errors.append(
            checks.Warning(
                "CORS_EXPOSE_HEADERS must be sequence",
                id="django-cors-headers.W008"
            )
        )
    if not isinstance(corsheaders_settings.CORS_URLS_REGEX, str):
        errors.append(
            checks.Warning(
                "CORS_URLS_REGEX must be regex string",
                id="django-cors-headers.W009"
            )
        )
    if corsheaders_settings.CORS_MODEL and not isinstance(corsheaders_settings.CORS_MODEL, str):
        errors.append(
            checks.Warning(
                "CORS_MODEL must be string",
                id="django-cors-headers.W0010"
            )
        )
    if not isinstance(corsheaders_settings.CORS_REPLACE_HTTPS_REFERER, bool):
        errors.append(
            checks.Warning(
                "CORS_REPLACE_HTTPS_REFERER must be bool",
                id="django-cors-headers.W0011"
            )
        )
    return errors