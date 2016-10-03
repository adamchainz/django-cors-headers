from django.test import SimpleTestCase
from django.utils import six

from corsheaders.models import CorsModel


class CorsModelTests(SimpleTestCase):

    def test_str(self):
        instance = CorsModel(cors='foo')
        assert six.text_type(instance) == 'foo'
