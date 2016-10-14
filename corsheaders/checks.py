import collections
import numbers

from django.core import checks

from .conf import corsheaders_settings


@checks.register
def check_settings(app_configs, **kwargs):

    errors = []
    if not isinstance(corsheaders_settings.CORS_ALLOW_HEADERS, collections.Sequence):
        errors.append(
            checks.Error(
                "CORS_ALLOW_HEADERS must be sequence",
                id="corsheaders.E001"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ALLOW_METHODS, collections.Sequence):
        errors.append(
            checks.Error(
                "CORS_ALLOW_METHODS must be sequence",
                id="corsheaders.E002"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ALLOW_CREDENTIALS, bool):
        errors.append(
            checks.Error(
                "CORS_ALLOW_CREDENTIALS must be bool",
                id="corsheaders.E003"
            )
        )

    if not isinstance(corsheaders_settings.CORS_PREFLIGHT_MAX_AGE, numbers.Integral) or \
            (corsheaders_settings.CORS_PREFLIGHT_MAX_AGE < 0):
        errors.append(
            checks.Error(
                "CORS_PREFLIGHT_MAX_AGE must be integer and must be greater than or equal to zero",
                id="corsheaders.E004"
            )
        )

    if not isinstance(corsheaders_settings.CORS_ORIGIN_ALLOW_ALL, bool):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_ALLOW_ALL must be bool",
                id="corsheaders.E005"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ORIGIN_WHITELIST, collections.Sequence):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_WHITELIST must be sequence",
                id="corsheaders.E006"
            )
        )
    if not isinstance(corsheaders_settings.CORS_ORIGIN_REGEX_WHITELIST, collections.Sequence):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_REGEX_WHITELIST must be sequence",
                id="corsheaders.E007"
            )
        )
    if not isinstance(corsheaders_settings.CORS_EXPOSE_HEADERS, collections.Sequence):
        errors.append(
            checks.Error(
                "CORS_EXPOSE_HEADERS must be sequence",
                id="corsheaders.E008"
            )
        )
    if not isinstance(corsheaders_settings.CORS_URLS_REGEX, str):
        errors.append(
            checks.Error(
                "CORS_URLS_REGEX must be regex string",
                id="corsheaders.E009"
            )
        )
    if corsheaders_settings.CORS_MODEL is not None and not isinstance(corsheaders_settings.CORS_MODEL, str):
        errors.append(
            checks.Error(
                "CORS_MODEL must be string",
                id="corsheaders.E0010"
            )
        )
    if not isinstance(corsheaders_settings.CORS_REPLACE_HTTPS_REFERER, bool):
        errors.append(
            checks.Error(
                "CORS_REPLACE_HTTPS_REFERER must be bool",
                id="corsheaders.E0011"
            )
        )
    return errors
