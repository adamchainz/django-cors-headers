from django.http import HttpResponse
from django.test import TestCase
from corsheaders.middleware import CorsMiddleware
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN
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

