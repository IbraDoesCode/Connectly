import os
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToPath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{ext}"
        return os.path.join("", new_filename)


# Create your models here.
class Media(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'

    MEDIA_TYPE_CHOICES = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    )

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=UploadToPath())
    metadata = models.JSONField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name