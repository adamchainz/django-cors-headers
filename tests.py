#!/usr/bin/env python
"""
"""
import sys


def run_tests():
    import django
    from django.conf import global_settings
    from django.conf import settings
    try:
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
            MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + (
                'corsheaders.middleware.CorsMiddleware',),
        )
    except TypeError:  # django 1.9+
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
            MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + [
                'corsheaders.middleware.CorsMiddleware',],
        )
    if hasattr(django, 'setup'):
        django.setup()

    try:
        from django.test.runner import DiscoverRunner as Runner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as Runner

    test_runner = Runner(verbosity=1)
    return test_runner.run_tests(['corsheaders'])


def main():
    failures = run_tests()
    sys.exit(failures)

if __name__ == '__main__':
    main()
