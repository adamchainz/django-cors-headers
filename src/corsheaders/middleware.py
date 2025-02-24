from __future__ import annotations

import re
from collections.abc import Awaitable
from typing import Callable
from urllib.parse import SplitResult
from urllib.parse import urlsplit

from asgiref.sync import iscoroutinefunction
from asgiref.sync import markcoroutinefunction
from django.http import HttpRequest
from django.http import HttpResponse
from django.http.response import HttpResponseBase
from django.utils.cache import patch_vary_headers

from corsheaders.conf import conf
from corsheaders.signals import check_request_enabled

# Define both variants of headers
_HEADERS_LOWER = {
    "access-control-allow-origin": "access-control-allow-origin",
    "access-control-expose-headers": "access-control-expose-headers",
    "access-control-allow-credentials": "access-control-allow-credentials",
    "access-control-allow-headers": "access-control-allow-headers",
    "access-control-allow-methods": "access-control-allow-methods",
    "access-control-max-age": "access-control-max-age",
    "access-control-request-private-network": "access-control-request-private-network",
    "access-control-allow-private-network": "access-control-allow-private-network",
}

_HEADERS_PASCAL = {
    "access-control-allow-origin": "Access-Control-Allow-Origin",
    "access-control-expose-headers": "Access-Control-Expose-Headers",
    "access-control-allow-credentials": "Access-Control-Allow-Credentials",
    "access-control-allow-headers": "Access-Control-Allow-Headers",
    "access-control-allow-methods": "Access-Control-Allow-Methods",
    "access-control-max-age": "Access-Control-Max-Age",
    "access-control-request-private-network": "Access-Control-Request-Private-Network",
    "access-control-allow-private-network": "Access-Control-Allow-Private-Network",
}


# Use PascalCase or lowercase based on setting
def get_header_name(header_key: str) -> str:
    if conf.USE_PASCAL_CASE_FOR_HEADER_NAMES:
        return _HEADERS_PASCAL[header_key]
    return _HEADERS_LOWER[header_key]


ACCESS_CONTROL_ALLOW_ORIGIN = get_header_name("access-control-allow-origin")
ACCESS_CONTROL_EXPOSE_HEADERS = get_header_name("access-control-expose-headers")
ACCESS_CONTROL_ALLOW_CREDENTIALS = get_header_name("access-control-allow-credentials")
ACCESS_CONTROL_ALLOW_HEADERS = get_header_name("access-control-allow-headers")
ACCESS_CONTROL_ALLOW_METHODS = get_header_name("access-control-allow-methods")
ACCESS_CONTROL_MAX_AGE = get_header_name("access-control-max-age")
ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK = get_header_name(
    "access-control-request-private-network"
)
ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK = get_header_name(
    "access-control-allow-private-network"
)


class CorsMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            # Mark the class as async-capable, but do the actual switch

            # inside __call__ to avoid swapping out dunder methods
            markcoroutinefunction(self)

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(request)
        response: HttpResponseBase | None = self.check_preflight(request)
        if response is None:
            result = self.get_response(request)
            assert isinstance(result, HttpResponseBase)
            response = result
        self.add_response_headers(request, response)
        return response

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        response = self.check_preflight(request)
        if response is None:
            result = self.get_response(request)
            assert not isinstance(result, HttpResponseBase)
            response = await result
        self.add_response_headers(request, response)
        return response

    def check_preflight(self, request: HttpRequest) -> HttpResponseBase | None:
        """
        Generate a response for CORS preflight requests.
        """
        request._cors_enabled = self.is_enabled(request)  # type: ignore [attr-defined]
        if (
            request._cors_enabled  # type: ignore [attr-defined]
            and request.method == "OPTIONS"
            and "access-control-request-method" in request.headers
        ):
            return HttpResponse(headers={"content-length": "0"})
        return None

    def add_response_headers(
        self, request: HttpRequest, response: HttpResponseBase
    ) -> HttpResponseBase:
        """
        Add the respective CORS headers
        """
        enabled = getattr(request, "_cors_enabled", None)
        if enabled is None:
            enabled = self.is_enabled(request)

        if not enabled:
            return response

        patch_vary_headers(response, ("origin",))

        origin = request.headers.get("origin")
        if not origin:
            return response

        try:
            url = urlsplit(origin)
        except ValueError:
            return response

        if (
            not conf.CORS_ALLOW_ALL_ORIGINS
            and not self.origin_found_in_white_lists(origin, url)
            and not self.check_signal(request)
        ):
            return response

        if conf.CORS_ALLOW_ALL_ORIGINS and not conf.CORS_ALLOW_CREDENTIALS:
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
        else:
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

        if conf.CORS_ALLOW_CREDENTIALS:
            response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"

        if len(conf.CORS_EXPOSE_HEADERS):
            response[ACCESS_CONTROL_EXPOSE_HEADERS] = ", ".join(
                conf.CORS_EXPOSE_HEADERS
            )

        if request.method == "OPTIONS":
            response[ACCESS_CONTROL_ALLOW_HEADERS] = ", ".join(conf.CORS_ALLOW_HEADERS)
            response[ACCESS_CONTROL_ALLOW_METHODS] = ", ".join(conf.CORS_ALLOW_METHODS)
            if conf.CORS_PREFLIGHT_MAX_AGE:
                response[ACCESS_CONTROL_MAX_AGE] = str(conf.CORS_PREFLIGHT_MAX_AGE)

        if (
            conf.CORS_ALLOW_PRIVATE_NETWORK
            and request.headers.get(ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK) == "true"
        ):
            response[ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK] = "true"

        return response

    def origin_found_in_white_lists(self, origin: str, url: SplitResult) -> bool:
        return (
            (origin == "null" and origin in conf.CORS_ALLOWED_ORIGINS)
            or self._url_in_whitelist(url)
            or self.regex_domain_match(origin)
        )

    def regex_domain_match(self, origin: str) -> bool:
        return any(
            re.match(domain_pattern, origin)
            for domain_pattern in conf.CORS_ALLOWED_ORIGIN_REGEXES
        )

    def is_enabled(self, request: HttpRequest) -> bool:
        return bool(
            re.match(conf.CORS_URLS_REGEX, request.path_info)
        ) or self.check_signal(request)

    def check_signal(self, request: HttpRequest) -> bool:
        signal_responses = check_request_enabled.send(sender=None, request=request)
        return any(return_value for function, return_value in signal_responses)

    def _url_in_whitelist(self, url: SplitResult) -> bool:
        origins = [urlsplit(o) for o in conf.CORS_ALLOWED_ORIGINS]
        return any(
            origin.scheme == url.scheme and origin.netloc == url.netloc
            for origin in origins
        )
