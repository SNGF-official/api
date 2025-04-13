import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from sngf_api.core.models import Status
from sngf_api.files.models import FileModel


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    miniature = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    published_at = models.DateTimeField(blank=True, null=True)
    file = models.ForeignKey(
        FileModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
        help_text="Fichier téléchargeable de l'article",
    )
    status = models.CharField(max_length=10, choices=Status.STATUS)

    def __str__(self):
        return self.title
