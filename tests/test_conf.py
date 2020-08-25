from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.conf import conf


class ConfTests(SimpleTestCase):
    @override_settings(CORS_ALLOW_HEADERS=["foo"])
    def test_can_override(self):
        assert conf.CORS_ALLOW_HEADERS == ["foo"]

    @override_settings(CORS_ORIGIN_ALLOW_ALL=True)
    def test_cors_allow_all_origins_old_alias(self):
        assert conf.CORS_ALLOW_ALL_ORIGINS is True

    @override_settings(
        CORS_ALLOW_ALL_ORIGINS=False,
        CORS_ORIGIN_ALLOW_ALL=True,
    )
    def test_cors_allow_all_origins_new_setting_takes_precedence(self):
        assert conf.CORS_ALLOW_ALL_ORIGINS is False

    @override_settings(CORS_ORIGIN_WHITELIST=["example.com"])
    def test_cors_allowed_origins_old_alias(self):
        assert conf.CORS_ALLOWED_ORIGINS == ["example.com"]

    @override_settings(
        CORS_ALLOWED_ORIGINS=["example.com"], CORS_ORIGIN_WHITELIST=["example.org"]
    )
    def test_cors_allowed_origins_new_setting_takes_precedence(self):
        assert conf.CORS_ALLOWED_ORIGINS == ["example.com"]

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=[r".*"])
    def test_cors_allowed_origin_regexes_old_alias(self):
        assert conf.CORS_ALLOWED_ORIGIN_REGEXES == [".*"]

    @override_settings(
        CORS_ALLOWED_ORIGIN_REGEXES=["a+"], CORS_ORIGIN_REGEX_WHITELIST=[".*"]
    )
    def test_cors_allowed_origin_regexes_new_setting_takes_precedence(self):
        assert conf.CORS_ALLOWED_ORIGIN_REGEXES == ["a+"]
