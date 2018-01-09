from __future__ import absolute_import

from contextlib import contextmanager

import django
from django.test.utils import modify_settings

from corsheaders.signals import check_request_enabled


def add_middleware(action, path):
    if django.VERSION[:2] >= (1, 10):
        middleware_setting = 'MIDDLEWARE'
    else:
        middleware_setting = 'MIDDLEWARE_CLASSES'

    return modify_settings(**{
        middleware_setting: {
            action: path,
        }
    })


def append_middleware(path):
    return add_middleware('append', path)


def prepend_middleware(path):
    return add_middleware('prepend', path)


@contextmanager
def temporary_check_request_hander(handler):
    check_request_enabled.connect(handler)
    try:
        yield
    finally:
        check_request_enabled.disconnect(handler)
