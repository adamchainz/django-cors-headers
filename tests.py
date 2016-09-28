#!/usr/bin/env python
"""
"""
import sys


def run_tests():
    import django
    from django.conf import global_settings, settings
    from django.test.runner import DiscoverRunner

    middleware = list(global_settings.MIDDLEWARE_CLASSES)
    middleware.append('corsheaders.middleware.CorsMiddleware')

    settings.configure(
        INSTALLED_APPS=[
            'corsheaders',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': ':memory:',
            },
        },
        MIDDLEWARE_CLASSES=middleware,
    )
    django.setup()

    test_runner = DiscoverRunner(verbosity=1)
    return test_runner.run_tests(['corsheaders'])


def main():
    failures = run_tests()
    sys.exit(failures)

if __name__ == '__main__':
    main()
