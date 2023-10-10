from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from typing import Pattern
from typing import Sequence

from django.conf import settings as _django_settings

from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods


@dataclass
class Settings:
    CORS_ALLOW_HEADERS: Sequence[str] = default_headers
    CORS_ALLOW_METHODS: Sequence[str] = default_methods
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_PRIVATE_NETWORK: bool = False
    CORS_PREFLIGHT_MAX_AGE: int = 86400
    CORS_ALLOW_ALL_ORIGINS: bool = False
    CORS_ALLOWED_ORIGINS: list[str] | tuple[str] = ()  # type: ignore
    CORS_ALLOWED_ORIGIN_REGEXES: Sequence[str | Pattern[str]] = ()
    CORS_EXPOSE_HEADERS: Sequence[str] = ()
    CORS_URLS_REGEX: str | Pattern[str] = re.compile(r"^.*$")


_RENAMED_SETTINGS = {
    # New name -> Old name
    "CORS_ALLOW_ALL_ORIGINS": "CORS_ORIGIN_ALLOW_ALL",
    "CORS_ALLOWED_ORIGINS": "CORS_ORIGIN_WHITELIST",
    "CORS_ALLOWED_ORIGIN_REGEXES": "CORS_ORIGIN_REGEX_WHITELIST",
}


class DjangoConfig(Settings):
    """
    A version of Settings that prefers to read from Django's settings.

    Falls back to its own values if the setting is not configured
    in Django.
    """

    def __getattribute__(self, name: str) -> Any:
        default = object.__getattribute__(self, name)
        if name in _RENAMED_SETTINGS:
            # Renamed settings are used if the new setting
            # is not configured in Django,
            old_name = _RENAMED_SETTINGS[name]
            default = getattr(_django_settings, old_name, default)
        return getattr(_django_settings, name, default)


conf = DjangoConfig()
