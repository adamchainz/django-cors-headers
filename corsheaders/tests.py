from django.http import HttpResponse
from django.test import TestCase
from corsheaders.middleware import CorsMiddleware, CorsPostCsrfMiddleware
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN
from corsheaders.middleware import ACCESS_CONTROL_EXPOSE_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_CREDENTIALS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_METHODS
from corsheaders.middleware import ACCESS_CONTROL_MAX_AGE
from corsheaders import defaults as settings
from mock import Mock
from mock import patch


class settings_override(object):
    def __init__(self, **kwargs):
        self.overrides = kwargs

    def __enter__(self):
        self.old = dict((key, getattr(settings, key)) for key in self.overrides)
        settings.__dict__.update(self.overrides)

    def __exit__(self, exc, value, tb):
        settings.__dict__.update(self.old)


class TestCorsMiddlewareProcessRequest(TestCase):

    def setUp(self):
        self.middleware = CorsMiddleware()

    def test_process_request(self):
        request = Mock(path='/')
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': 'value'}
        with settings_override(CORS_URLS_REGEX='^.*$'):
            response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponse)

    def test_process_request_empty_header(self):
        request = Mock(path='/')
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': ''}
        with settings_override(CORS_URLS_REGEX='^.*$'):
            response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponse)

    def test_process_request_no_header(self):
        request = Mock(path='/')
        request.method = 'OPTIONS'
        request.META = {}
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

    def test_process_request_not_options(self):
        request = Mock(path='/')
        request.method = 'GET'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': 'value'}
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

    def test_process_request_replace_https_referer(self):
        post_middleware = CorsPostCsrfMiddleware()
        request = Mock(path='/')
        request.method = 'GET'
        request.is_secure = lambda: True

        # make sure it doesnt blow up when HTTP_REFERER is not present
        request.META = {
            'HTTP_HOST': 'foobar.com',
            'HTTP_ORIGIN': 'https://foo.google.com',
        }
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)

        # make sure it doesnt blow up when HTTP_HOST is not present
        request.META = {
            'HTTP_REFERER': 'http://foo.google.com/',
            'HTTP_ORIGIN': 'https://foo.google.com',
        }
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)

        request.is_secure = lambda: False
        request.META = {
            'HTTP_REFERER': 'http://foo.google.com/',
            'HTTP_HOST': 'foobar.com',
            'HTTP_ORIGIN': 'http://foo.google.com',
        }

        # test that we won't replace if the request is not secure
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'http://foo.google.com/')

        request.is_secure = lambda: True
        request.META = {
            'HTTP_REFERER': 'https://foo.google.com/',
            'HTTP_HOST': 'foobar.com',
            'HTTP_ORIGIN': 'https://foo.google.com',
        }

        # test that we won't replace with the setting off
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*'):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        # make sure the replace code is idempotent
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_view(request, None, None, None)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        with settings_override(CORS_URLS_REGEX='^.*$', CORS_REPLACE_HTTPS_REFERER=True):
            post_middleware.process_request(request)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        with settings_override(CORS_URLS_REGEX='^.*$', CORS_REPLACE_HTTPS_REFERER=True):
            response = post_middleware.process_request(request)
        self.assertIsNone(response)

    def test_process_view_replace_https_referer(self):
        post_middleware = CorsPostCsrfMiddleware()
        request = Mock(path='/')
        request.method = 'GET'
        request.is_secure = lambda: True
        request.META = {
            'HTTP_REFERER': 'https://foo.google.com/',
            'HTTP_HOST': 'foobar.com',
            'HTTP_ORIGIN': 'https://foo.google.com',
        }
        with settings_override(CORS_URLS_REGEX='^.*$',
                               CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
                               CORS_REPLACE_HTTPS_REFERER=True):
            response = self.middleware.process_view(request, None, None, None)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        with settings_override(CORS_URLS_REGEX='^.*$', CORS_REPLACE_HTTPS_REFERER=True):
            post_middleware.process_view(request, None, None, None)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        with settings_override(CORS_URLS_REGEX='^.*$', CORS_REPLACE_HTTPS_REFERER=True):
            response = post_middleware.process_view(request, None, None, None)
        self.assertIsNone(response)


@patch('corsheaders.middleware.settings')
class TestCorsMiddlewareProcessResponse(TestCase):

    def setUp(self):
        self.middleware = CorsMiddleware()

    def assertAccessControlAllowOriginEquals(self, response, header):
        self.assertIn(ACCESS_CONTROL_ALLOW_ORIGIN, response, "Response %r does "
            "NOT have %r header" % (response, ACCESS_CONTROL_ALLOW_ORIGIN))
        self.assertEqual(response[ACCESS_CONTROL_ALLOW_ORIGIN], header)

    def test_process_response_no_origin(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    def test_process_response_not_in_whitelist(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ORIGIN_WHITELIST = ['example.com']
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    def test_process_response_in_whitelist(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ORIGIN_WHITELIST = ['example.com', 'foobar.it']
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertAccessControlAllowOriginEquals(processed, 'http://foobar.it')

    def test_process_response_expose_headers(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_EXPOSE_HEADERS = ['accept', 'origin', 'content-type']
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_EXPOSE_HEADERS],
            'accept, origin, content-type')

    def test_process_response_dont_expose_headers(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_EXPOSE_HEADERS = []
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_EXPOSE_HEADERS, processed)

    def test_process_response_allow_credentials(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_CREDENTIALS = True
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_CREDENTIALS], 'true')

    def test_process_response_dont_allow_credentials(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_CREDENTIALS = False
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_CREDENTIALS, processed)

    def test_process_response_options_method(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_HEADERS = ['content-type', 'origin']
        settings.CORS_ALLOW_METHODS = ['GET', 'OPTIONS']
        settings.CORS_PREFLIGHT_MAX_AGE = 1002
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_HEADERS],
            'content-type, origin')
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertEqual(processed[ACCESS_CONTROL_MAX_AGE], '1002')

    def test_process_response_options_method_no_max_age(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_HEADERS = ['content-type', 'origin']
        settings.CORS_ALLOW_METHODS = ['GET', 'OPTIONS']
        settings.CORS_PREFLIGHT_MAX_AGE = 0
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_HEADERS],
            'content-type, origin')
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertNotIn(ACCESS_CONTROL_MAX_AGE, processed)

    def test_process_response_whitelist_with_port(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        settings.CORS_ORIGIN_WHITELIST = ('localhost:9000',)
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://localhost:9000'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_CREDENTIALS, None), 'true')

    def test_process_response_adds_origin_when_domain_found_in_origin_regex_whitelist(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_REGEX_WHITELIST = ('^http?://(\w+\.)?google\.com$', )
        settings.CORS_ALLOW_CREDENTIALS = True
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), 'http://foo.google.com')

    def test_process_response_will_not_add_origin_when_domain_not_found_in_origin_regex_whitelist(self, settings):
        settings.CORS_MODEL = None
        settings.CORS_ORIGIN_REGEX_WHITELIST = ('^http?://(\w+\.)?yahoo\.com$', )
        settings.CORS_ALLOW_CREDENTIALS = True
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        settings.CORS_URLS_REGEX = '^.*$'
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), None)

    def test_process_response_when_custom_model_enabled(self, settings):
        from corsheaders.models import CorsModel
        CorsModel.objects.create(cors='foo.google.com')
        settings.CORS_ORIGIN_REGEX_WHITELIST = ()
        settings.CORS_ALLOW_CREDENTIALS = False
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = settings.default_methods
        settings.CORS_URLS_REGEX = '^.*$'
        settings.CORS_MODEL = 'corsheaders.CorsModel'
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foo.google.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), 'http://foo.google.com')
