from __future__ import annotations

import asyncio
import re
from typing import Awaitable
from typing import Callable
from urllib.parse import SplitResult
from urllib.parse import urlsplit

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBase
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from corsheaders.conf import conf
from corsheaders.signals import check_request_enabled

ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"


class CorsMiddleware(MiddlewareMixin):
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
        if asyncio.iscoroutinefunction(self.get_response):
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            self._is_coroutine = (
                asyncio.coroutines._is_coroutine  # type: ignore [attr-defined]
            )
        else:
            self._is_coroutine = None

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self._is_coroutine:
            return self.__acall__(request)
        response = self.check_preflight(request)
        if response is None:
            response = self.get_response(request)
            assert isinstance(response, HttpResponseBase)
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

    def check_preflight(self, request: HttpRequest) -> HttpResponse | None:
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
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """
        Add the respective CORS headers
        """
        enabled = getattr(request, "_cors_enabled", None)
        if enabled is None:
            enabled = self.is_enabled(request)

        if not enabled:
            return response

        patch_vary_headers(response, ("Origin",))

        origin = request.headers.get("origin")
        if not origin:
            return response

        try:
            url = urlsplit(origin)
        except ValueError:
            return response

        if conf.CORS_ALLOW_CREDENTIALS:
            response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"

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

        if len(conf.CORS_EXPOSE_HEADERS):
            response[ACCESS_CONTROL_EXPOSE_HEADERS] = ", ".join(
                conf.CORS_EXPOSE_HEADERS
            )

        if request.method == "OPTIONS":
            response[ACCESS_CONTROL_ALLOW_HEADERS] = ", ".join(conf.CORS_ALLOW_HEADERS)
            response[ACCESS_CONTROL_ALLOW_METHODS] = ", ".join(conf.CORS_ALLOW_METHODS)
            if conf.CORS_PREFLIGHT_MAX_AGE:
                response[ACCESS_CONTROL_MAX_AGE] = str(conf.CORS_PREFLIGHT_MAX_AGE)

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
