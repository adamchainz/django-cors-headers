from django.http import HttpResponse
from django.test import TestCase
from corsheaders.middleware import CorsMiddleware
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN
from corsheaders.middleware import ACCESS_CONTROL_EXPOSE_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_CREDENTIALS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_METHODS
from corsheaders.middleware import ACCESS_CONTROL_MAX_AGE
from mock import Mock
from mock import patch


class TestCorsMiddlewareProcessRequest(TestCase):

    def setUp(self):
        self.middleware = CorsMiddleware()

    def test_process_request(self):
        request = Mock()
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': 'value'}
        response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponse)

    def test_process_request_empty_header(self):
        request = Mock()
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': ''}
        response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponse)

    def test_process_request_no_header(self):
        request = Mock()
        request.method = 'OPTIONS'
        request.META = {}
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

    def test_process_request_not_options(self):
        request = Mock()
        request.method = 'GET'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': 'value'}
        response = self.middleware.process_request(request)
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
        response = HttpResponse()
        request = Mock(META={})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    def test_process_response_not_in_whitelist(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ORIGIN_WHITELIST = ['example.com']
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    def test_process_response_in_whitelist(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ORIGIN_WHITELIST = ['example.com', 'foobar.it']
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertAccessControlAllowOriginEquals(processed, 'http://foobar.it')

    def test_process_response_expose_headers(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_EXPOSE_HEADERS = ['accept', 'origin', 'content-type']
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_EXPOSE_HEADERS],
            'accept, origin, content-type')

    def test_process_response_dont_expose_headers(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_EXPOSE_HEADERS = []
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_EXPOSE_HEADERS, processed)

    def test_process_response_allow_credentials(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_CREDENTIALS = True
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_CREDENTIALS], 'true')

    def test_process_response_dont_allow_credentials(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_CREDENTIALS = False
        response = HttpResponse()
        request = Mock(META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_CREDENTIALS, processed)

    def test_process_response_options_method(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_HEADERS = ['content-type', 'origin']
        settings.CORS_ALLOW_METHODS = ['GET', 'OPTIONS']
        settings.CORS_PREFLIGHT_MAX_AGE = 1002
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_HEADERS],
            'content-type, origin')
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertEqual(processed[ACCESS_CONTROL_MAX_AGE], '1002')

    def test_process_response_options_method_no_max_age(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = True
        settings.CORS_ALLOW_HEADERS = ['content-type', 'origin']
        settings.CORS_ALLOW_METHODS = ['GET', 'OPTIONS']
        settings.CORS_PREFLIGHT_MAX_AGE = 0
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_HEADERS],
            'content-type, origin')
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertNotIn(ACCESS_CONTROL_MAX_AGE, processed)

    def test_process_response_whitelist_with_port(self, settings):
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        settings.CORS_ORIGIN_WHITELIST = ('localhost:9000',)
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://localhost:9000'}
        request = Mock(META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_CREDENTIALS), 'true')

    def test_process_response_adds_origin_when_domain_found_in_origin_regex_whitelist(self, settings):
        settings.CORS_ORIGIN_REGEX_WHITELIST = ('^http?://(\w+\.)?google\.com$', )
        settings.CORS_ALLOW_CREDENTIALS = True
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN), 'http://foo.google.com')

    def test_process_response_will_not_add_origin_when_domain_not_found_in_origin_regex_whitelist(self, settings):
        settings.CORS_ORIGIN_REGEX_WHITELIST = ('^http?://(\w+\.)?yahoo\.com$', )
        settings.CORS_ALLOW_CREDENTIALS = True
        settings.CORS_ORIGIN_ALLOW_ALL = False
        settings.CORS_ALLOW_METHODS = ['OPTIONS']
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN), None)
