from django.db import models


class AbstractCorsModel(models.Model):
    class Meta:
        abstract = True
        db_table = 'corsheaders_corsmodel'

    cors = models.CharField(max_length=255)
