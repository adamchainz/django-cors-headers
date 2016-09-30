from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.conf import corsheaders_settings


class ConfTests(SimpleTestCase):

    @override_settings(CORS_ALLOW_HEADERS=['foo'])
    def test_can_override(self):
        assert corsheaders_settings.CORS_ALLOW_HEADERS == ['foo']
