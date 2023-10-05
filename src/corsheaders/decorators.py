from __future__ import annotations

import asyncio
import functools
from typing import Any
from typing import Callable
from typing import cast
from typing import TypeVar

from django.http import HttpRequest
from django.http.response import HttpResponseBase

from corsheaders.conf import conf as _conf
from corsheaders.conf import Settings
from corsheaders.middleware import CorsMiddleware

F = TypeVar("F", bound=Callable[..., HttpResponseBase])


def cors(func: F | None = None, *, conf: Settings = _conf) -> F | Callable[[F], F]:
    if func is None:
        return cast(Callable[[F], F], functools.partial(cors, conf=conf))

    assert callable(func)

    if asyncio.iscoroutinefunction(func):

        async def inner(
            _request: HttpRequest, *args: Any, **kwargs: Any
        ) -> HttpResponseBase:
            async def get_response(request: HttpRequest) -> HttpResponseBase:
                return await func(request, *args, **kwargs)

            return await CorsMiddleware(get_response, conf=conf)(_request)

    else:

        def inner(_request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
            def get_response(request: HttpRequest) -> HttpResponseBase:
                return func(request, *args, **kwargs)

            return CorsMiddleware(get_response, conf=conf)(_request)

    wrapper = functools.wraps(func)(inner)
    wrapper._skip_cors_middleware = True  # type: ignore [attr-defined]
    return cast(F, wrapper)
