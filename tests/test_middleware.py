from __future__ import annotations

from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.deprecation import MiddlewareMixin

from corsheaders.middleware import ACCESS_CONTROL_ALLOW_CREDENTIALS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_METHODS
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN
from corsheaders.middleware import ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK
from corsheaders.middleware import ACCESS_CONTROL_EXPOSE_HEADERS
from corsheaders.middleware import ACCESS_CONTROL_MAX_AGE
from tests.utils import prepend_middleware
from tests.utils import temporary_check_request_hander


class ShortCircuitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return HttpResponse("short-circuit-middleware-response")


class CorsMiddlewareTests(TestCase):
    def test_get_no_origin(self):
        resp = self.client.get("/")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    def test_get_origin_vary_by_default(self):
        resp = self.client.get("/")
        assert resp["vary"] == "origin"

    def test_get_invalid_origin(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com]")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_get_not_in_allowed_origins(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.org")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(CORS_ALLOWED_ORIGINS=["http://example.org"])
    def test_get_not_in_allowed_origins_due_to_wrong_scheme(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.org")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com", "https://example.org"]
    )
    def test_get_in_allowed_origins(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.org")
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.org"

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.org"])
    async def test_async_get_in_allowed_origins(self):
        resp = await self.async_client.get("/async/", origin="https://example.org")
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.org"

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com", "null"])
    def test_null_in_allowed_origins(self):
        resp = self.client.get("/", HTTP_ORIGIN="null")
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "null"

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com", "file://"])
    def test_file_in_allowed_origins(self):
        """
        'file://' should be allowed as an origin since Chrome on Android
        mistakenly sends it
        """
        resp = self.client.get("/", HTTP_ORIGIN="file://")
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "file://"

    @override_settings(
        CORS_ALLOW_ALL_ORIGINS=True,
        CORS_EXPOSE_HEADERS=["accept", "content-type"],
    )
    def test_get_expose_headers(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert resp[ACCESS_CONTROL_EXPOSE_HEADERS] == "accept, content-type"

    @override_settings(CORS_ALLOW_ALL_ORIGINS=True)
    def test_get_dont_expose_headers(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_EXPOSE_HEADERS not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_ALLOW_CREDENTIALS=True
    )
    def test_get_allow_credentials(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert resp[ACCESS_CONTROL_ALLOW_CREDENTIALS] == "true"

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_ALLOW_CREDENTIALS=True
    )
    def test_get_allow_credentials_bad_origin(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.org")
        assert ACCESS_CONTROL_ALLOW_CREDENTIALS not in resp

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_get_allow_credentials_disabled(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_CREDENTIALS not in resp

    @override_settings(CORS_ALLOW_PRIVATE_NETWORK=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_allow_private_network_added_if_enabled_and_requested(self):
        resp = self.client.get(
            "/",
            HTTP_ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK="true",
            HTTP_ORIGIN="http://example.com",
        )
        assert resp[ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK] == "true"

    @override_settings(CORS_ALLOW_PRIVATE_NETWORK=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_allow_private_network_not_added_if_enabled_and_not_requested(self):
        resp = self.client.get("/", HTTP_ORIGIN="http://example.com")
        assert ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK not in resp

    @override_settings(
        CORS_ALLOW_PRIVATE_NETWORK=True,
        CORS_ALLOWED_ORIGINS=["http://example.com"],
    )
    def test_allow_private_network_not_added_if_enabled_and_no_cors_origin(self):
        resp = self.client.get(
            "/",
            HTTP_ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK="true",
            HTTP_ORIGIN="http://example.org",
        )
        assert ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK not in resp

    @override_settings(CORS_ALLOW_PRIVATE_NETWORK=False, CORS_ALLOW_ALL_ORIGINS=True)
    def test_allow_private_network_not_added_if_disabled_and_requested(self):
        resp = self.client.get(
            "/",
            HTTP_ACCESS_CONTROL_REQUEST_PRIVATE_NETWORK="true",
            HTTP_ORIGIN="http://example.com",
        )
        assert ACCESS_CONTROL_ALLOW_PRIVATE_NETWORK not in resp

    @override_settings(
        CORS_ALLOW_HEADERS=["content-type"],
        CORS_ALLOW_METHODS=["GET", "OPTIONS"],
        CORS_PREFLIGHT_MAX_AGE=1002,
        CORS_ALLOW_ALL_ORIGINS=True,
    )
    def test_options_allowed_origin(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp.status_code == HTTPStatus.OK
        assert resp[ACCESS_CONTROL_ALLOW_HEADERS] == "content-type"
        assert resp[ACCESS_CONTROL_ALLOW_METHODS] == "GET, OPTIONS"
        assert resp[ACCESS_CONTROL_MAX_AGE] == "1002"

    @override_settings(
        CORS_ALLOW_HEADERS=["content-type"],
        CORS_ALLOW_METHODS=["GET", "OPTIONS"],
        CORS_PREFLIGHT_MAX_AGE=1002,
        CORS_ALLOW_ALL_ORIGINS=True,
    )
    async def test_async_options_allowed_origin(self):
        resp = await self.async_client.options(
            "/async/",
            origin="https://example.com",
            access_control_request_method="GET",
        )
        assert resp.status_code == HTTPStatus.OK
        assert resp[ACCESS_CONTROL_ALLOW_HEADERS] == "content-type"
        assert resp[ACCESS_CONTROL_ALLOW_METHODS] == "GET, OPTIONS"
        assert resp[ACCESS_CONTROL_MAX_AGE] == "1002"

    @override_settings(
        CORS_ALLOW_HEADERS=["content-type"],
        CORS_ALLOW_METHODS=["GET", "OPTIONS"],
        CORS_PREFLIGHT_MAX_AGE=0,
        CORS_ALLOW_ALL_ORIGINS=True,
    )
    def test_options_no_max_age(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_HEADERS] == "content-type"
        assert resp[ACCESS_CONTROL_ALLOW_METHODS] == "GET, OPTIONS"
        assert ACCESS_CONTROL_MAX_AGE not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://localhost:9000"],
    )
    def test_options_allowed_origins_with_port(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://localhost:9000",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://localhost:9000"

    @override_settings(
        CORS_ALLOWED_ORIGIN_REGEXES=[r"^https://\w+\.example\.com$"],
    )
    def test_options_adds_origin_when_domain_found_in_allowed_regexes(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://foo.example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://foo.example.com"

    @override_settings(
        CORS_ALLOWED_ORIGIN_REGEXES=[
            r"^https://\w+\.example\.org$",
            r"^https://\w+\.example\.com$",
        ],
    )
    def test_options_adds_origin_when_domain_found_in_allowed_regexes_second(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://foo.example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://foo.example.com"

    @override_settings(
        CORS_ALLOWED_ORIGIN_REGEXES=[r"^https://\w+\.example\.org$"],
    )
    def test_options_doesnt_add_origin_when_domain_not_found_in_allowed_regexes(
        self,
    ):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://foo.example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    def test_options_empty_request_method(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="",
        )
        assert resp.status_code == HTTPStatus.OK

    def test_options_no_headers(self):
        resp = self.client.options("/")
        assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @override_settings(CORS_ALLOW_CREDENTIALS=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_allow_all_origins_get(self):
        resp = self.client.get(
            "/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp.status_code == HTTPStatus.OK
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp["vary"] == "origin"

    @override_settings(CORS_ALLOW_CREDENTIALS=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_allow_all_origins_options(self):
        resp = self.client.options(
            "/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp.status_code == HTTPStatus.OK
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp["vary"] == "origin"

    @override_settings(CORS_ALLOW_CREDENTIALS=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_non_200_headers_still_set(self):
        """
        It's not clear whether the header should still be set for non-HTTP200
        when not a preflight request. However this is the existing behaviour for
        django-cors-middleware, so at least this test makes that explicit, especially
        since for the switch to Django 1.10, special-handling will need to be put in
        place to preserve this behaviour. See `ExceptionMiddleware` mention here:
        https://docs.djangoproject.com/en/3.0/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware  # noqa: E501
        """
        resp = self.client.get("/unauthorized/", HTTP_ORIGIN="https://example.com")
        assert resp.status_code == HTTPStatus.UNAUTHORIZED
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"

    @override_settings(CORS_ALLOW_CREDENTIALS=True, CORS_ALLOW_ALL_ORIGINS=True)
    def test_auth_view_options(self):
        """
        Ensure HTTP200 and header still set, for preflight requests to views requiring
        authentication. See: https://github.com/adamchainz/django-cors-headers/issues/3
        """
        resp = self.client.options(
            "/test-401/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp.status_code == HTTPStatus.OK
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp["Content-Length"] == "0"

    def test_signal_handler_that_returns_false(self):
        def handler(*args, **kwargs):
            return False

        with temporary_check_request_hander(handler):
            resp = self.client.options(
                "/",
                HTTP_ORIGIN="https://example.com",
                HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
            )

            assert resp.status_code == HTTPStatus.OK
            assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    def test_signal_handler_that_returns_true(self):
        def handler(*args, **kwargs):
            return True

        with temporary_check_request_hander(handler):
            resp = self.client.options(
                "/",
                HTTP_ORIGIN="https://example.com",
                HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
            )
            assert resp.status_code == HTTPStatus.OK
            assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_signal_handler_allow_some_urls_to_everyone(self):
        def allow_api_to_all(sender, request, **kwargs):
            return request.path.startswith("/api/")

        with temporary_check_request_hander(allow_api_to_all):
            resp = self.client.options(
                "/",
                HTTP_ORIGIN="https://example.org",
                HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
            )
            assert resp.status_code == HTTPStatus.OK
            assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

            resp = self.client.options(
                "/api/something/",
                HTTP_ORIGIN="https://example.org",
                HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
            )
            assert resp.status_code == HTTPStatus.OK
            assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.org"

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_signal_called_once_during_normal_flow(self):
        calls = 0

        def allow_all(sender, request, **kwargs):
            nonlocal calls
            calls += 1
            return True

        with temporary_check_request_hander(allow_all):
            self.client.get("/", HTTP_ORIGIN="https://example.org")

            assert calls == 1

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    @prepend_middleware(f"{__name__}.ShortCircuitMiddleware")
    def test_get_short_circuit(self):
        """
        Test a scenario when a middleware that returns a response is run before
        the ``CorsMiddleware``. In this case
        ``CorsMiddleware.process_response()`` should ignore the request if
        MIDDLEWARE setting is used (new mechanism in Django 1.10+).
        """
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_URLS_REGEX=r"^/foo/$"
    )
    @prepend_middleware(f"{__name__}.ShortCircuitMiddleware")
    def test_get_short_circuit_should_be_ignored(self):
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_URLS_REGEX=r"^/foo/$"
    )
    def test_get_regex_matches(self):
        resp = self.client.get("/foo/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_ORIGIN in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_URLS_REGEX=r"^/not-foo/$"
    )
    def test_get_regex_doesnt_match(self):
        resp = self.client.get("/foo/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp

    @override_settings(
        CORS_ALLOWED_ORIGINS=["https://example.com"], CORS_URLS_REGEX=r"^/foo/$"
    )
    def test_get_regex_matches_path_info(self):
        resp = self.client.get(
            "/foo/", HTTP_ORIGIN="https://example.com", SCRIPT_NAME="/prefix/"
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN in resp

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_cors_enabled_is_attached_and_bool(self):
        """
        Ensure that request._cors_enabled is available - although a private API
        someone might use it for debugging
        """
        resp = self.client.get("/", HTTP_ORIGIN="https://example.com")
        request = resp.wsgi_request
        assert isinstance(request._cors_enabled, bool)  # type: ignore [attr-defined]
        assert request._cors_enabled  # type: ignore [attr-defined]

    @override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
    def test_works_if_view_deletes_cors_enabled(self):
        """
        Just in case something crazy happens in the view or other middleware,
        check that get_response doesn't fall over if `_cors_enabled` is removed
        """
        resp = self.client.get("/delete-enabled/", HTTP_ORIGIN="https://example.com")
        assert ACCESS_CONTROL_ALLOW_ORIGIN in resp
