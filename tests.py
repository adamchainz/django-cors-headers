#!/usr/bin/env python
"""
"""
import sys


def run_tests():
    import django
    from django.conf import global_settings, settings
    from django.test.runner import DiscoverRunner

    if django.VERSION >= (1, 10):
        middleware_setting = 'MIDDLEWARE'
    else:
        middleware_setting = 'MIDDLEWARE_CLASSES'

    middleware = list(global_settings.MIDDLEWARE_CLASSES)
    middleware.append('corsheaders.middleware.CorsMiddleware')

    config = {
        'INSTALLED_APPS': [
            'corsheaders',
        ],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': ':memory:',
            },
        },
        'ROOT_URLCONF': 'corsheaders.tests.urls',
        middleware_setting: middleware,
    }
    settings.configure(**config)
    django.setup()

    test_runner = DiscoverRunner(verbosity=1)
    return test_runner.run_tests(['corsheaders'])


def main():
    failures = run_tests()
    sys.exit(failures)

if __name__ == '__main__':
    main()
