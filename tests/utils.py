import django
from django.test.utils import modify_settings


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
