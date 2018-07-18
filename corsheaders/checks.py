from __future__ import absolute_import

import re
from collections import Sequence
from numbers import Integral

from django.core import checks
from django.utils import six

from .conf import conf

re_type = type(re.compile(''))


check_list = [
    (
        lambda: not is_sequence(conf.CORS_ALLOW_HEADERS, six.string_types),
        'CORS_ALLOW_HEADERS should be a sequence of strings.',
        'corsheaders.E001',
    ),
    (
        lambda: not is_sequence(conf.CORS_ALLOW_METHODS, six.string_types),
        'CORS_ALLOW_METHODS should be a sequence of strings.',
        'corsheaders.E002',
    ),
    (
        lambda: not isinstance(conf.CORS_ALLOW_CREDENTIALS, bool),
        'CORS_ALLOW_CREDENTIALS should be a bool.',
        'corsheaders.E003',
    ),
    (
        lambda: not isinstance(conf.CORS_PREFLIGHT_MAX_AGE, Integral) or conf.CORS_PREFLIGHT_MAX_AGE < 0,
        'CORS_PREFLIGHT_MAX_AGE should be an integer greater than or equal to zero.',
        'corsheaders.E004',
    ),
    (
        lambda: not isinstance(conf.CORS_ORIGIN_ALLOW_ALL, bool),
        'CORS_ORIGIN_ALLOW_ALL should be a bool.',
        'corsheaders.E005',
    ),
    (
        lambda: not is_sequence(conf.CORS_ORIGIN_WHITELIST, six.string_types),
        'CORS_ORIGIN_WHITELIST should be a sequence of strings.',
        'corsheaders.E006',
    ),
    (
        lambda: not is_sequence(conf.CORS_ORIGIN_REGEX_WHITELIST, six.string_types + (re_type,)),
        'CORS_ORIGIN_REGEX_WHITELIST should be a sequence of strings and/or compiled regexes.',
        'corsheaders.E007',
    ),
    (
        lambda: not is_sequence(conf.CORS_EXPOSE_HEADERS, six.string_types),
        'CORS_EXPOSE_HEADERS should be a sequence.',
        'corsheaders.E008',
    ),
    (
        lambda: not isinstance(conf.CORS_URLS_REGEX, six.string_types + (re_type,)),
        'CORS_URLS_REGEX should be a string or regex.',
        'corsheaders.E009',
    ),
    (
        lambda: conf.CORS_MODEL is not None and not isinstance(conf.CORS_MODEL, six.string_types),
        'CORS_MODEL should be a string or None.',
        'corsheaders.E010',
    ),
    (
        lambda: not isinstance(conf.CORS_REPLACE_HTTPS_REFERER, bool),
        'CORS_REPLACE_HTTPS_REFERER should be a bool.',
        'corsheaders.E011',
    ),
    (
        lambda: not isinstance(conf.CORS_ORIGIN_CREDENTIALS_ALLOW_ALL, bool),
        'CORS_ORIGIN_CREDENTIALS_ALLOW_ALL should be a bool.',
        'corsheaders.E012',
    ),
    (
        lambda: not is_sequence(conf.CORS_ORIGIN_CREDENTIALS_WHITELIST, six.string_types),
        'CORS_ORIGIN_CREDENTIALS_WHITELIST should be a sequence of strings.',
        'corsheaders.E013',
    ),
    (
        lambda: not is_sequence(conf.CORS_ORIGIN_CREDENTIALS_REGEX_WHITELIST, six.string_types + (re_type,)),
        'CORS_ORIGIN_CREDENTIALS_REGEX_WHITELIST should be a sequence of strings and/or compiled regexes.',
        'corsheaders.E014',
    ),
]


def check_cors_allow_headers():
    return


@checks.register
def check_settings(app_configs, **kwargs):
    errors = []
    for check in check_list:
        check_func, error_message, check_id = check
        if check_func():
            errors.append(checks.Error(
                error_message,
                id=check_id
            ))

    return errors


def is_sequence(thing, types):
    return (
        isinstance(thing, Sequence) and
        all(isinstance(x, types) for x in thing)
    )
