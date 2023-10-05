from __future__ import annotations

from typing import cast
from typing import List
from typing import Pattern
from typing import Sequence
from typing import Tuple
from typing import Union

from django.conf import settings

from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods


class Settings:
    """
    Shadow Django's settings with a little logic
    """

    @property
    def CORS_ALLOW_HEADERS(self) -> Sequence[str]:
        return getattr(settings, "CORS_ALLOW_HEADERS", default_headers)

    @property
    def CORS_ALLOW_METHODS(self) -> Sequence[str]:
        return getattr(settings, "CORS_ALLOW_METHODS", default_methods)

    @property
    def CORS_ALLOW_CREDENTIALS(self) -> bool:
        return getattr(settings, "CORS_ALLOW_CREDENTIALS", False)

    @property
    def CORS_ALLOW_PRIVATE_NETWORK(self) -> bool:
        return getattr(settings, "CORS_ALLOW_PRIVATE_NETWORK", False)

    @property
    def CORS_PREFLIGHT_MAX_AGE(self) -> int:
        return getattr(settings, "CORS_PREFLIGHT_MAX_AGE", 86400)

    @property
    def CORS_ALLOW_ALL_ORIGINS(self) -> bool:
        return getattr(
            settings,
            "CORS_ALLOW_ALL_ORIGINS",
            getattr(settings, "CORS_ORIGIN_ALLOW_ALL", False),
        )

    @property
    def CORS_ALLOWED_ORIGINS(self) -> list[str] | tuple[str]:
        value = getattr(
            settings,
            "CORS_ALLOWED_ORIGINS",
            getattr(settings, "CORS_ORIGIN_WHITELIST", ()),
        )
        return cast(Union[List[str], Tuple[str]], value)

    @property
    def CORS_ALLOWED_ORIGIN_REGEXES(self) -> Sequence[str | Pattern[str]]:
        return getattr(
            settings,
            "CORS_ALLOWED_ORIGIN_REGEXES",
            getattr(settings, "CORS_ORIGIN_REGEX_WHITELIST", ()),
        )

    @property
    def CORS_EXPOSE_HEADERS(self) -> Sequence[str]:
        return getattr(settings, "CORS_EXPOSE_HEADERS", ())

    @property
    def CORS_URLS_REGEX(self) -> str | Pattern[str]:
        return getattr(settings, "CORS_URLS_REGEX", r"^.*$")


conf = Settings()
