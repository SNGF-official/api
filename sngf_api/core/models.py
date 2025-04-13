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


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class Contactable(models.Model):
    name = models.CharField(max_length=100, blank=True)
    customer_email = models.EmailField(blank=True)

    class Meta:
        abstract = True
