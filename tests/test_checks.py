from django.test import SimpleTestCase
from django.test.utils import override_settings
from django.core import checks

from corsheaders.conf import corsheaders_settings
from corsheaders.checks import check_settings

from corsheaders.defaults import default_headers, default_methods

class SettingsTests(SimpleTestCase):

    @override_settings(CORS_ALLOW_HEADERS=True)
    def test_cors_allow_headers_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W001"

    @override_settings(CORS_ALLOW_METHODS=1)
    def test_cors_allow_methods_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W002"

    @override_settings(CORS_ALLOW_CREDENTIALS=())
    def test_cors_allow_credentials_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W003"

    @override_settings(CORS_PREFLIGHT_MAX_AGE="10")
    def test_cors_preflight_max_age_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W004"

    @override_settings(CORS_ORIGIN_ALLOW_ALL=0)
    def test_cors_origin_allow_all_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W005"

    @override_settings(CORS_ORIGIN_WHITELIST=True)
    def test_cors_origin_whitelist_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W006"

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=10)
    def test_cors_origin_regex_whitelist_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W007"

    @override_settings(CORS_EXPOSE_HEADERS=True)
    def test_cors_expose_headers_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W008"

    @override_settings(CORS_URLS_REGEX=())
    def test_cors_urls_regex_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W009"

    @override_settings(CORS_MODEL=())
    def test_cors_model_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W0010"

    @override_settings(CORS_REPLACE_HTTPS_REFERER=())
    def test_cors_replace_https_referer_failure(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W0011"

    @override_settings(CORS_ALLOW_HEADERS=default_headers)
    def test_cors_allow_headers_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_ALLOW_METHODS=default_methods)
    def test_cors_allow_methods_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_ALLOW_CREDENTIALS=True)
    def test_cors_allow_credentials_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_PREFLIGHT_MAX_AGE=86400)
    def test_cors_preflight_max_age_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_ORIGIN_ALLOW_ALL=True)
    def test_cors_origin_allow_all_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_ORIGIN_WHITELIST=())
    def test_cors_origin_whitelist_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_ORIGIN_REGEX_WHITELIST=())
    def test_cors_origin_regex_whitelist_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_EXPOSE_HEADERS=())
    def test_cors_expose_headers_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_URLS_REGEX=r'^.*$')
    def test_cors_urls_regex_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_MODEL=None)
    def test_cors_model_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_REPLACE_HTTPS_REFERER=True)
    def test_cors_replace_https_referer_success(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) == 0

    @override_settings(CORS_PREFLIGHT_MAX_AGE=-1)
    def test_cors_preflight_max_age_negative(self):
        errors = check_settings(corsheaders_settings)
        assert len(errors) > 0
        assert isinstance(errors[0], checks.Error)
        assert errors[0].id == "corsheaders.W004.1"