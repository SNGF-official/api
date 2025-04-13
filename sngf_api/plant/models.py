import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from sngf_api.core.models import Status


class PlantImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plant = models.ForeignKey("Plant", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="plants/gallery/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image de {self.plant.name}"


class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        SEED = "SEED", "Graines"
        PLANT = "PLANT", "Plante"

    class SizeChoices(models.TextChoices):
        XS = "XS", "Très petit"
        S = "S", "Petit"
        M = "M", "Moyen"
        L = "L", "Grand"
        XL = "XL", "Très grand"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=10, choices=CategoryChoices.choices, null=False
    )
    type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=5, choices=SizeChoices.choices, null=False)
    status = models.CharField(max_length=10, choices=Status.STATUS)

    def __str__(self):
        return self.name
