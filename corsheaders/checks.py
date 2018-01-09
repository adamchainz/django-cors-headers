from __future__ import absolute_import

import re
from collections import Sequence
from numbers import Integral

from django.core import checks
from django.utils import six

from .conf import conf

re_type = type(re.compile(''))


@checks.register
def check_settings(app_configs, **kwargs):
    errors = []

    if not is_sequence(conf.CORS_ALLOW_HEADERS, six.string_types):
        errors.append(
            checks.Error(
                "CORS_ALLOW_HEADERS should be a sequence of strings.",
                id="corsheaders.E001"
            )
        )

    if not is_sequence(conf.CORS_ALLOW_METHODS, six.string_types):
        errors.append(
            checks.Error(
                "CORS_ALLOW_METHODS should be a sequence of strings.",
                id="corsheaders.E002"
            )
        )

    if not isinstance(conf.CORS_ALLOW_CREDENTIALS, bool):
        errors.append(
            checks.Error(
                "CORS_ALLOW_CREDENTIALS should be a bool.",
                id="corsheaders.E003"
            )
        )

    if not isinstance(conf.CORS_PREFLIGHT_MAX_AGE, Integral) or conf.CORS_PREFLIGHT_MAX_AGE < 0:
        errors.append(
            checks.Error(
                "CORS_PREFLIGHT_MAX_AGE should be an integer greater than or equal to zero.",
                id="corsheaders.E004"
            )
        )

    if not isinstance(conf.CORS_ORIGIN_ALLOW_ALL, bool):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_ALLOW_ALL should be a bool.",
                id="corsheaders.E005"
            )
        )

    if not is_sequence(conf.CORS_ORIGIN_WHITELIST, six.string_types):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_WHITELIST should be a sequence of strings.",
                id="corsheaders.E006"
            )
        )

    if not is_sequence(conf.CORS_ORIGIN_REGEX_WHITELIST, six.string_types + (re_type,)):
        errors.append(
            checks.Error(
                "CORS_ORIGIN_REGEX_WHITELIST should be a sequence of strings and/or compiled regexes.",
                id="corsheaders.E007"
            )
        )

    if not is_sequence(conf.CORS_EXPOSE_HEADERS, six.string_types):
        errors.append(
            checks.Error(
                "CORS_EXPOSE_HEADERS should be a sequence.",
                id="corsheaders.E008"
            )
        )

    if not isinstance(conf.CORS_URLS_REGEX, six.string_types + (re_type,)):
        errors.append(
            checks.Error(
                "CORS_URLS_REGEX should be a string or regex.",
                id="corsheaders.E009"
            )
        )

    if conf.CORS_MODEL is not None and not isinstance(conf.CORS_MODEL, six.string_types):
        errors.append(
            checks.Error(
                "CORS_MODEL should be a string or None.",
                id="corsheaders.E010"
            )
        )

    if not isinstance(conf.CORS_REPLACE_HTTPS_REFERER, bool):
        errors.append(
            checks.Error(
                "CORS_REPLACE_HTTPS_REFERER should be a bool.",
                id="corsheaders.E011"
            )
        )

    return errors


def is_sequence(thing, types):
    return (
        isinstance(thing, Sequence) and
        all(isinstance(x, types) for x in thing)
    )
