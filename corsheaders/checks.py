from __future__ import absolute_import

import re
from numbers import Integral

from django.conf import settings
from django.core import checks
from django.utils import six
from django.utils.six.moves.urllib.parse import urlparse

from corsheaders.conf import conf

try:
    from collections.abc import Sequence  # Python 3.3+
except ImportError:  # pragma: no cover
    from collections import Sequence

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
    else:
        for origin in conf.CORS_ORIGIN_WHITELIST:
            if origin == 'null':
                continue
            parsed = urlparse(origin)
            if parsed.scheme == '' or parsed.netloc == '':
                errors.append(checks.Error(
                    "Origin {} in CORS_ORIGIN_WHITELIST is missing scheme or netloc".format(repr(origin)),
                    id="corsheaders.E013"
                ))
            else:
                # Only do this check in this case because if the scheme is not provided, netloc ends up in path
                for part in ('path', 'params', 'query', 'fragment'):
                    if getattr(parsed, part) != '':
                        errors.append(checks.Error(
                            "Origin {} in CORS_ORIGIN_WHITELIST should not have {}".format(repr(origin), part),
                            id="corsheaders.E014"
                        ))

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

    if not isinstance(conf.CORS_REPLACE_HTTPS_REFERER, bool):
        errors.append(
            checks.Error(
                "CORS_REPLACE_HTTPS_REFERER should be a bool.",
                id="corsheaders.E011"
            )
        )

    if hasattr(settings, 'CORS_MODEL'):
        errors.append(
            checks.Error(
                "The CORS_MODEL setting has been removed - see django-cors-headers' HISTORY.",
                id="corsheaders.E012"
            )
        )

    return errors


def is_sequence(thing, types):
    return (
        isinstance(thing, Sequence)
        and all(isinstance(x, types) for x in thing)
    )
