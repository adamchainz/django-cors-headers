from __future__ import absolute_import

from django.test import SimpleTestCase
from django.test.utils import override_settings

from corsheaders.conf import conf


class ConfTests(SimpleTestCase):

    @override_settings(CORS_ALLOW_HEADERS=['foo'])
    def test_can_override(self):
        assert conf.CORS_ALLOW_HEADERS == ['foo']
