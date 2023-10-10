from __future__ import annotations

from django.test import TestCase
from django.test.utils import modify_settings
from django.test.utils import override_settings

from corsheaders.middleware import ACCESS_CONTROL_ALLOW_ORIGIN


@modify_settings(
    MIDDLEWARE={
        "remove": "corsheaders.middleware.CorsMiddleware",
    }
)
@override_settings(CORS_ALLOWED_ORIGINS=["https://example.com"])
class CorsDecoratorsTestCase(TestCase):
    def test_get_no_origin(self):
        resp = self.client.get("/decorated/hello/")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Decorated: hello"

    def test_get_not_in_allowed_origins(self):
        resp = self.client.get(
            "/decorated/hello/",
            HTTP_ORIGIN="https://example.net",
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Decorated: hello"

    def test_get_in_allowed_origins_preflight(self):
        resp = self.client.options(
            "/decorated/hello/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b""

    def test_get_in_allowed_origins(self):
        resp = self.client.get(
            "/decorated/hello/",
            HTTP_ORIGIN="https://example.com",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b"Decorated: hello"

    async def test_async_get_not_in_allowed_origins(self):
        resp = await self.async_client.get(
            "/async-decorated/hello/",
            origin="https://example.org",
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Async Decorated: hello"

    async def test_async_get_in_allowed_origins_preflight(self):
        resp = await self.async_client.options(
            "/async-decorated/hello/",
            origin="https://example.com",
            access_control_request_method="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b""

    async def test_async_get_in_allowed_origins(self):
        resp = await self.async_client.get(
            "/async-decorated/hello/",
            origin="https://example.com",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b"Async Decorated: hello"


class CorsDecoratorsWithConfTestCase(TestCase):
    def test_get_no_origin(self):
        resp = self.client.get("/decorated-with-conf/hello/")
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Decorated (with conf): hello"

    def test_get_not_in_allowed_origins(self):
        resp = self.client.get(
            "/decorated-with-conf/hello/",
            HTTP_ORIGIN="https://example.net",
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Decorated (with conf): hello"

    def test_get_in_allowed_origins_preflight(self):
        resp = self.client.options(
            "/decorated-with-conf/hello/",
            HTTP_ORIGIN="https://example.com",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b""

    def test_get_in_allowed_origins(self):
        resp = self.client.get(
            "/decorated-with-conf/hello/",
            HTTP_ORIGIN="https://example.com",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b"Decorated (with conf): hello"

    async def test_async_get_not_in_allowed_origins(self):
        resp = await self.async_client.get(
            "/async-decorated-with-conf/hello/",
            origin="https://example.org",
        )
        assert ACCESS_CONTROL_ALLOW_ORIGIN not in resp
        assert resp.content == b"Async Decorated (with conf): hello"

    async def test_async_get_in_allowed_origins_preflight(self):
        resp = await self.async_client.options(
            "/async-decorated-with-conf/hello/",
            origin="https://example.com",
            access_control_request_method="GET",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b""

    async def test_async_get_in_allowed_origins(self):
        resp = await self.async_client.get(
            "/async-decorated-with-conf/hello/",
            origin="https://example.com",
        )
        assert resp[ACCESS_CONTROL_ALLOW_ORIGIN] == "https://example.com"
        assert resp.content == b"Async Decorated (with conf): hello"
