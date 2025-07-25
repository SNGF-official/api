import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from sngf_api.core.models import Status


class EventModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.TextField(max_length=250, null=False, help_text="NB: N'ajoutez en aucun cas des émojies")
    description = models.TextField(blank=True, help_text="NB: N'ajoutez en aucun cas des émojies")
    status = models.CharField(max_length=20, choices=Status.STATUS)
    date = models.DateTimeField(null=False)
    location = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )

    def __str__(self):
        return self.title
