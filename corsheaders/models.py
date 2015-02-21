from django.db import models


class CorsModel(models.Model):
    cors = models.CharField(max_length=255)
