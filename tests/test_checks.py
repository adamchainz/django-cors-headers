import pytest
from django.core import checks
from django.core.management import base, call_command
from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.checks import check_settings


class ChecksTests(SimpleTestCase):

    @override_settings(CORS_ALLOW_HEADERS=True)
    def test_cors_allow_headers_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E001"

    @override_settings(CORS_ALLOW_METHODS=1)
    def test_cors_allow_methods_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E002"

    @override_settings(CORS_ALLOW_CREDENTIALS=())
    def test_cors_allow_credentials_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E003"

    @override_settings(CORS_PREFLIGHT_MAX_AGE="10")
    def test_cors_preflight_max_age_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E004"

    @override_settings(CORS_ORIGIN_ALLOW_ALL=0)
    def test_cors_origin_allow_all_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E005"

    @override_settings(CORS_ORIGIN_WHITELIST=True)
    def test_cors_origin_whitelist_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E006"

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=10)
    def test_cors_origin_regex_whitelist_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E007"

    @override_settings(CORS_EXPOSE_HEADERS=True)
    def test_cors_expose_headers_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E008"

    @override_settings(CORS_URLS_REGEX=())
    def test_cors_urls_regex_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E009"

    @override_settings(CORS_MODEL=())
    def test_cors_model_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E0010"

    @override_settings(CORS_REPLACE_HTTPS_REFERER=())
    def test_cors_replace_https_referer_failure(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E0011"

    @override_settings(CORS_PREFLIGHT_MAX_AGE=-1)
    def test_cors_preflight_max_age_negative(self):
        errors = check_settings([])
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.E004"

    def test_all_pass(self):
        errors = check_settings([])
        assert len(errors) == 0

    @override_settings(CORS_ORIGIN_ALLOW_ALL=0)
    def test_call_command(self):
        with pytest.raises(base.SystemCheckError):
            call_command('check')
