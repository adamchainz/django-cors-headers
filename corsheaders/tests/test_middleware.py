from django.http import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings

from corsheaders.middleware import CorsMiddleware, CorsPostCsrfMiddleware
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN
from corsheaders.middleware import ACCESS_CONTROL_EXPOSE_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_CREDENTIALS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_METHODS
from corsheaders.middleware import ACCESS_CONTROL_MAX_AGE
from corsheaders import defaults as settings
from mock import Mock


class TestCorsMiddlewareProcessRequest(TestCase):

    def setUp(self):
        self.middleware = CorsMiddleware()

    @override_settings(CORS_URLS_REGEX='^.*$')
    def test_process_request(self):
        request = Mock(path='/')
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': 'value'}
        response = self.middleware.process_request(request)
        self.assertIsInstance(response, HttpResponse)

    @override_settings(CORS_URLS_REGEX='^.*$')
    def test_process_request_empty_header(self):
        request = Mock(path='/')
        request.method = 'OPTIONS'
        request.META = {'HTTP_ACCESS_CONTROL_REQUEST_METHOD': ''}
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

    @override_settings(
        CORS_URLS_REGEX='^.*$',
        CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
        CORS_REPLACE_HTTPS_REFERER=True,
    )
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
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

        # make sure it doesnt blow up when HTTP_HOST is not present
        request.META = {
            'HTTP_REFERER': 'http://foo.google.com/',
            'HTTP_ORIGIN': 'https://foo.google.com',
        }
        response = self.middleware.process_request(request)
        self.assertIsNone(response)

        request.is_secure = lambda: False
        request.META = {
            'HTTP_REFERER': 'http://foo.google.com/',
            'HTTP_HOST': 'foobar.com',
            'HTTP_ORIGIN': 'http://foo.google.com',
        }

        # test that we won't replace if the request is not secure
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
        with override_settings(CORS_REPLACE_HTTPS_REFERER=False):
            response = self.middleware.process_request(request)
        self.assertIsNone(response)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        response = self.middleware.process_request(request)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        # make sure the replace code is idempotent
        response = self.middleware.process_view(request, None, None, None)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        post_middleware.process_request(request)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        response = post_middleware.process_request(request)
        self.assertIsNone(response)

    @override_settings(
        CORS_ORIGIN_REGEX_WHITELIST='.*google.*',
        CORS_REPLACE_HTTPS_REFERER=True,
    )
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
        response = self.middleware.process_view(request, None, None, None)
        self.assertIsNone(response)
        self.assertEquals(request.META['ORIGINAL_HTTP_REFERER'], 'https://foo.google.com/')
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foobar.com/')

        post_middleware.process_view(request, None, None, None)
        self.assertTrue('ORIGINAL_HTTP_REFERER' not in request.META)
        self.assertEquals(request.META['HTTP_REFERER'], 'https://foo.google.com/')

        response = post_middleware.process_view(request, None, None, None)
        self.assertIsNone(response)


# @patch('corsheaders.middleware.settings')
class TestCorsMiddlewareProcessResponse(TestCase):

    def setUp(self):
        self.middleware = CorsMiddleware()

    def assertAccessControlAllowOriginEquals(self, response, header):
        self.assertIn(
            ACCESS_CONTROL_ALLOW_ORIGIN,
            response,
            "Response %r does NOT have %r header" % (response, ACCESS_CONTROL_ALLOW_ORIGIN)
        )
        self.assertEqual(response[ACCESS_CONTROL_ALLOW_ORIGIN], header)

    @override_settings(
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_no_origin(self):
        response = HttpResponse()
        request = Mock(path='/', META={})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    @override_settings(
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_WHITELIST=['example.com'],
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_not_in_whitelist(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_ORIGIN, processed)

    @override_settings(
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_WHITELIST=['example.com', 'foobar.it'],
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_in_whitelist(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foobar.it'})
        processed = self.middleware.process_response(request, response)
        self.assertAccessControlAllowOriginEquals(processed, 'http://foobar.it')

    @override_settings(
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_EXPOSE_HEADERS=['accept', 'origin', 'content-type'],
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_expose_headers(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(
            processed[ACCESS_CONTROL_EXPOSE_HEADERS],
            'accept, origin, content-type'
        )

    @override_settings(
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_EXPOSE_HEADERS=[],
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_dont_expose_headers(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_EXPOSE_HEADERS, processed)

    @override_settings(
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_allow_credentials(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_CREDENTIALS], 'true')

    @override_settings(
        CORS_ALLOW_CREDENTIALS=False,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_dont_allow_credentials(self):
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://example.com'})
        processed = self.middleware.process_response(request, response)
        self.assertNotIn(ACCESS_CONTROL_ALLOW_CREDENTIALS, processed)

    @override_settings(
        CORS_ALLOW_HEADERS=['content-type', 'origin'],
        CORS_ALLOW_METHODS=['GET', 'OPTIONS'],
        CORS_PREFLIGHT_MAX_AGE=1002,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_options_method(self):
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_HEADERS], 'content-type, origin')
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertEqual(processed[ACCESS_CONTROL_MAX_AGE], '1002')

    @override_settings(
        CORS_ALLOW_HEADERS=['content-type', 'origin'],
        CORS_ALLOW_METHODS=['GET', 'OPTIONS'],
        CORS_PREFLIGHT_MAX_AGE=0,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_options_method_no_max_age(self):
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://example.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(
            processed[ACCESS_CONTROL_ALLOW_HEADERS],
            'content-type, origin'
        )
        self.assertEqual(processed[ACCESS_CONTROL_ALLOW_METHODS], 'GET, OPTIONS')
        self.assertNotIn(ACCESS_CONTROL_MAX_AGE, processed)

    @override_settings(
        CORS_ALLOW_METHODS=['OPTIONS'],
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_WHITELIST=('localhost:9000',),
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_whitelist_with_port(self):
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://localhost:9000'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_CREDENTIALS, None), 'true')

    @override_settings(
        CORS_ALLOW_METHODS=['OPTIONS'],
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_REGEX_WHITELIST=('^http?://(\w+\.)?google\.com$',),
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_adds_origin_when_domain_found_in_origin_regex_whitelist(self):
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), 'http://foo.google.com')

    @override_settings(
        CORS_ALLOW_METHODS=['OPTIONS'],
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_REGEX_WHITELIST=('^http?://(\w+\.)?yahoo\.com$',),
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_process_response_will_not_add_origin_when_domain_not_found_in_origin_regex_whitelist(self):
        response = HttpResponse()
        request_headers = {'HTTP_ORIGIN': 'http://foo.google.com'}
        request = Mock(path='/', META=request_headers, method='OPTIONS')
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), None)

    @override_settings(
        CORS_ALLOW_METHODS=settings.default_methods,
        CORS_ALLOW_CREDENTIALS=False,
        CORS_ORIGIN_ALLOW_ALL=False,
        CORS_ORIGIN_REGEX_WHITELIST=(),
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL='corsheaders.CorsModel',
    )
    def test_process_response_when_custom_model_enabled(self):
        from corsheaders.models import CorsModel
        CorsModel.objects.create(cors='foo.google.com')
        response = HttpResponse()
        request = Mock(path='/', META={'HTTP_ORIGIN': 'http://foo.google.com'})
        processed = self.middleware.process_response(request, response)
        self.assertEqual(processed.get(ACCESS_CONTROL_ALLOW_ORIGIN, None), 'http://foo.google.com')

    @override_settings(
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_middleware_integration_get(self):
        response = self.client.get('/test-view/', HTTP_ORIGIN='http://foobar.it')
        self.assertEqual(response.status_code, 200)
        self.assertAccessControlAllowOriginEquals(response, 'http://foobar.it')

    @override_settings(
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_middleware_integration_get_auth_view(self):
        """
        It's not clear whether the header should still be set for non-HTTP200
        when not a preflight request. However this is the existing behaviour for
        django-cors-middleware, so at least this test makes that explicit, especially
        since for the switch to Django 1.10, special-handling will need to be put in
        place to preserve this behaviour. See `ExceptionMiddleware` mention here:
        https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
        """
        response = self.client.get('/test-view-http401/', HTTP_ORIGIN='http://foobar.it')
        self.assertEqual(response.status_code, 401)
        self.assertAccessControlAllowOriginEquals(response, 'http://foobar.it')

    @override_settings(
        CORS_ALLOW_CREDENTIALS=True,
        CORS_ORIGIN_ALLOW_ALL=True,
        CORS_URLS_REGEX='^.*$',
        CORS_MODEL=None,
    )
    def test_middleware_integration_preflight_auth_view(self):
        """
        Ensure HTTP200 and header still set, for preflight requests to views requiring
        authentication. See: https://github.com/ottoyiu/django-cors-headers/issues/3
        """
        response = self.client.options('/test-view-http401/',
                                       HTTP_ORIGIN='http://foobar.it',
                                       HTTP_ACCESS_CONTROL_REQUEST_METHOD='value')
        self.assertEqual(response.status_code, 200)
        self.assertAccessControlAllowOriginEquals(response, 'http://foobar.it')
