from contextlib import contextmanager

import django
from django.test.utils import modify_settings

from corsheaders.signals import check_request_enabled


def append_middleware(path):
    if django.VERSION[:2] >= (1, 10):
        middleware_setting = 'MIDDLEWARE'
    else:
        middleware_setting = 'MIDDLEWARE_CLASSES'

    return modify_settings(**{
        middleware_setting: {
            'append': path
        }
    })


@contextmanager
def temporary_check_request_hander(handler):
    check_request_enabled.connect(handler)
    try:
        yield
    finally:
        check_request_enabled.disconnect(handler)
