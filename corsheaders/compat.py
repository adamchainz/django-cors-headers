try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # pragma: no cover
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object  # pragma: no cover
