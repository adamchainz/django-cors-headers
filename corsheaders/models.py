from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class CorsModel(models.Model):
    cors = models.CharField(max_length=255)

    def __str__(self):
        return self.cors
