from __future__ import annotations

from contextlib import contextmanager
from typing import Callable
from typing import Generator

from django.test.utils import modify_settings

from corsheaders.signals import check_request_enabled


def add_middleware(action: str, path: str) -> modify_settings:
    return modify_settings(**{"MIDDLEWARE": {action: path}})


def prepend_middleware(path: str) -> modify_settings:
    return add_middleware("prepend", path)


@contextmanager
def temporary_check_request_hander(
    handler: Callable[..., bool]
) -> Generator[None, None, None]:
    check_request_enabled.connect(handler)
    try:
        yield
    finally:
        check_request_enabled.disconnect(handler)
