from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.conf import conf


class ConfTests(SimpleTestCase):
    @override_settings(CORS_ALLOW_HEADERS=["foo"])
    def test_can_override(self):
        assert conf.CORS_ALLOW_HEADERS == ["foo"]

    @override_settings(
        CORS_ORIGIN_WHITELIST=["whitelist"], CORS_ORIGIN_ALLOWLIST=["allowlist"]
    )
    def test_allowlist_whitelist_priority(self):
        assert conf.CORS_ORIGIN_ALLOWLIST == ["allowlist"]

    @override_settings(CORS_ORIGIN_ALLOWLIST=["allowlist"])
    def test_allowlist_only(self):
        assert conf.CORS_ORIGIN_ALLOWLIST == ["allowlist"]

    @override_settings(CORS_ORIGIN_WHITELIST=["whitelist"])
    def test_whitelist_only(self):
        assert conf.CORS_ORIGIN_ALLOWLIST == ["whitelist"]
