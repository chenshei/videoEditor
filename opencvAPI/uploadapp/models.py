from os import path

from django.db import models
from opencvAPI import settings


class File(models.Model):
    file = models.FileField(upload_to=path.join(settings.MEDIA_ROOT, 'original'), blank=False, null=False)

    def __str__(self):
        return self.file.name
