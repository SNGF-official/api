import uuid

from django.db import models


class FileModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=250, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    file = models.FileField(upload_to="files", null=False)
    type = models.CharField(max_length=250, null=False)

    def __str__(self):
        return str(self.id)
