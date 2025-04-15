import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from sngf_api.core.models import Status


class PlantImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        "Plant", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="plants/gallery/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image de {self.product.name}"


class BaseProduct(models.Model):
    class CategoryChoices(models.TextChoices):
        AGROFORESTIERES = "AGROFORESTIERES", "Agroforestières"
        ENDEMIQUES_AUTOCHTONES = "ENDEMIQUES_AUTOCHTONES", "Endémiques autochtones"
        EXOTIQUES_REBOISEMENT = "EXOTIQUES_REBOISEMENT", "Exotiques de reboisement"
        ORNEMENTALES = "ORNEMENTALES", "Ornementales"
        EMBROUSSAILLEMENTS = "EMBROUSSAILLEMENTS", "Embrousseillements"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30, choices=CategoryChoices.choices, blank=True
    )
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.STATUS.choices)

    class Meta:
        abstract = True


class Seed(BaseProduct):
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.price_per_kilo}"


class Plant(BaseProduct):
    class SizeChoices(models.TextChoices):
        PM = "PM", "Petit modèle"
        MM = "MM", "Modèle moyen"
        GM = "GM", "Grand modèle"

    size = models.CharField(max_length=2, choices=SizeChoices.choices)

    prices = models.JSONField(
        help_text='Exemple : {"PM": 1500.00, "MM": 2500.00, "GM": 3500.00}'
    )

    def __str__(self):
        return f"{self.size}"
