import uuid

from django.db import models


class DummyModel(models.Model):
    """
    Used for test
    """

    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Status(models.Model):
    class STATUS(models.TextChoices):
        ACTIVE = ("ACTIVE", "active")
        INACTIVE = ("INACTIVE", "inactive")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    status = models.CharField(
        max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE
    )

    def __str__(self):
        return f"{self.id, self.status}"
