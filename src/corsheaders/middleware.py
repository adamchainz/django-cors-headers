from __future__ import annotations

import asyncio
import re
from typing import Any
from typing import Awaitable
from typing import Callable
from urllib.parse import SplitResult
from urllib.parse import urlsplit

from django.http import HttpRequest
from django.http import HttpResponse
from django.http.response import HttpResponseBase
from django.utils.cache import patch_vary_headers

from corsheaders.conf import conf
from corsheaders.conf import Settings
from corsheaders.signals import check_request_enabled

ACCESS_CONTROL_ALLOW_ORIGIN = "access-control-allow-origin"
ACCESS_CONTROL_EXPOSE_HEADERS = "access-control-expose-headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "access-control-allow-credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "access-control-allow-headers"
ACCESS_CONTROL_ALLOW_METHODS = "access-control-allow-methods"
ACCESS_CONTROL_MAX_AGE = "access-control-max-age"
ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK = "access-control-request-private-network"
ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK = "access-control-allow-private-network"


class CorsMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
        conf: Settings = conf,
    ) -> None:
        self.get_response = get_response
        self.conf = conf
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
        result = self.get_response(request)
        assert isinstance(result, HttpResponseBase)
        response = result
        if getattr(response, "_cors_processing_done", False):
            return response
        else:
            # Request wasn't processed (e.g. because of a 404)
            return self.add_response_headers(
                request, self.check_preflight(request) or response
            )

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        result = self.get_response(request)
        assert not isinstance(result, HttpResponseBase)
        response = await result
        if getattr(response, "_cors_processing_done", False):
            return response
        else:
            # View wasn't processed (e.g. because of a 404)
            return self.add_response_headers(
                request, self.check_preflight(request) or response
            )

    def process_view(
        self,
        request: HttpRequest,
        callback: Callable[[HttpRequest], HttpResponseBase],
        callback_args: Any,
        callback_kwargs: Any,
    ) -> HttpResponseBase | None:
        if getattr(callback, "_skip_cors_middleware", False):
            # View is decorated and will add CORS headers itself
            return None
        return self.check_preflight(request)

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
        response._cors_processing_done = True
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

        if self.conf.CORS_ALLOW_CREDENTIALS:
            response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"

        if (
            not self.conf.CORS_ALLOW_ALL_ORIGINS
            and not self.origin_found_in_white_lists(origin, url)
            and not self.check_signal(request)
        ):
            return response

        if self.conf.CORS_ALLOW_ALL_ORIGINS and not self.conf.CORS_ALLOW_CREDENTIALS:
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
        else:
            response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

        if len(self.conf.CORS_EXPOSE_HEADERS):
            response[ACCESS_CONTROL_EXPOSE_HEADERS] = ", ".join(
                self.conf.CORS_EXPOSE_HEADERS
            )

        if request.method == "OPTIONS":
            response[ACCESS_CONTROL_ALLOW_HEADERS] = ", ".join(
                self.conf.CORS_ALLOW_HEADERS
            )
            response[ACCESS_CONTROL_ALLOW_METHODS] = ", ".join(
                self.conf.CORS_ALLOW_METHODS
            )
            if self.conf.CORS_PREFLIGHT_MAX_AGE:
                response[ACCESS_CONTROL_MAX_AGE] = str(self.conf.CORS_PREFLIGHT_MAX_AGE)

        if (
            self.conf.CORS_ALLOW_PRIVATE_NETWORK
            and request.headers.get(ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK) == "true"
        ):
            response[ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK] = "true"

        return response

    def origin_found_in_white_lists(self, origin: str, url: SplitResult) -> bool:
        return (
            (origin == "null" and origin in self.conf.CORS_ALLOWED_ORIGINS)
            or self._url_in_whitelist(url)
            or self.regex_domain_match(origin)
        )

    def regex_domain_match(self, origin: str) -> bool:
        return any(
            re.match(domain_pattern, origin)
            for domain_pattern in self.conf.CORS_ALLOWED_ORIGIN_REGEXES
        )

    def is_enabled(self, request: HttpRequest) -> bool:
        return bool(
            re.match(self.conf.CORS_URLS_REGEX, request.path_info)
        ) or self.check_signal(request)

    def check_signal(self, request: HttpRequest) -> bool:
        signal_responses = check_request_enabled.send(sender=None, request=request)
        return any(return_value for function, return_value in signal_responses)

    def _url_in_whitelist(self, url: SplitResult) -> bool:
        origins = [urlsplit(o) for o in self.conf.CORS_ALLOWED_ORIGINS]
        return any(
            origin.scheme == url.scheme and origin.netloc == url.netloc
            for origin in origins
        )
