import django
from django.conf import global_settings

SECRET_KEY = 'NOTASECRET'

INSTALLED_APPS = [
    'corsheaders',
    'tests.testapp',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'TEST_NAME': ':memory:',
    },
}

ROOT_URLCONF = 'tests.urls'


middlewares = list(global_settings.MIDDLEWARE_CLASSES)
middlewares.append('corsheaders.middleware.CorsMiddleware')

if django.VERSION >= (1, 10):
    MIDDLEWARE = middlewares
else:
    MIDDLEWARE_CLASSES = middlewares

SECURE_PROXY_SSL_HEADER = ('HTTP_FAKE_SECURE', 'true')
