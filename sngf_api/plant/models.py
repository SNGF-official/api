import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from sngf_api.core.models import Status


class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique de l'image de la plante."
        "Il est généré automatiquement et ne peut pas être modifié.",
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        help_text="Code unique de la catégorie (par exemple, 'AGROFORESTIERES').",
    )
    display_name = models.CharField(  # noqa: DJ001
        max_length=100,
        blank=True,
        null=True,
        help_text="Nom affiché de la catégorie (par exemple, 'Agroforestières').",
    )

    def __str__(self):
        return self.display_name or self.name

    class Meta:  # noqa: DJ012
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class PlantImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique de l'image de la plante."
        "Il est généré automatiquement et ne peut pas être modifié.",
    )
    plant = models.ForeignKey(
        "Plant",
        related_name="images",
        on_delete=models.CASCADE,
        help_text="La plante à laquelle cette image est associée.",
    )
    image = models.ImageField(
        upload_to="plants/gallery/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        help_text="Le fichier image de la plante."
        "Les formats supportés sont JPG, JPEG, PNG et WEBP.",
        null=True,
    )
    image_url = models.CharField(  # noqa: DJ001
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Texte alternatif pour l'image,"
        "important pour l'accessibilité et le SEO.",
    )

    def __str__(self):
        return f"Image de {self.plant.name}"


class SeedImage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique de l'image de la graine."
        "Il est généré automatiquement et ne peut pas être modifié.",
    )
    seed = models.ForeignKey(
        "Seed",
        related_name="images",
        on_delete=models.CASCADE,
        help_text="La graîne à laquelle cette image est associée.",
    )
    image = models.ImageField(
        upload_to="seeds/gallery/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        help_text="Le fichier image de la plante."
        "Les formats supportés sont JPG, JPEG, PNG et WEBP.",
        null=True,
    )
    image_url = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Texte alternatif pour l'image,"
        "important pour l'accessibilité et le SEO.",
    )

    def __str__(self):
        return f"Image de {self.seed.name}"


class BaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique du produit de base."
        "Il est généré automatiquement et ne peut pas être modifié.",
    )
    name = models.CharField(max_length=100, help_text="Le nom du produit.")
    description = models.TextField(
        blank=True, help_text="Une description détaillée du produit (facultatif)."
    )
    quantity = models.PositiveIntegerField(
        help_text="La quantité disponible de ce produit."
    )
    status = models.CharField(
        max_length=10,
        choices=Status.STATUS.choices,
        help_text="Le statut actuel du produit "
        "(par exemple, 'Disponible', 'Indisponible').",
    )

    class Meta:
        abstract = True


class PlantSizePrice(models.Model):
    class SizeChoices(models.TextChoices):
        PM = "PM", "Petit modèle"
        MM = "MM", "Modèle moyen"
        GM = "GM", "Grand modèle"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique du prix par taille.",
    )
    plant = models.ForeignKey(
        "Plant",
        related_name="prices",
        on_delete=models.CASCADE,
        help_text="La plante à laquelle ce prix et cette taille sont associés.",
    )
    size = models.CharField(
        max_length=2, choices=SizeChoices.choices, help_text="La taille de la plante."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Le prix pour cette taille de plante.",
    )

    class Meta:
        unique_together = ("plant", "size")

    def __str__(self):
        return f"{self.plant.name} - {self.get_size_display()}: {self.price}"


class Plant(BaseProduct):
    categories = models.ManyToManyField(
        Category,
        related_name="plants",
        help_text="Les catégories auxquelles cette plante appartient.",
    )
    article_code = models.CharField(
        max_length=150,
        help_text="Code de l'article de la plante.",
    )
    scientific_name = models.CharField(
        max_length=100,
        help_text="Nom scientifique de la plante.",
    )
    species_code = models.CharField(
        max_length=150,
        help_text="Code de l'espèce de la plante.",
    )
    poids = models.PositiveIntegerField(
        default=9,
        help_text="1 = très important, 9 = peu important"
    )

    def __str__(self):
        return self.name


class Seed(BaseProduct):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique de la graine.",
    )
    name = models.CharField(max_length=100, help_text="Le nom des graines.")
    categories = models.ManyToManyField(
        Category,
        related_name="seeds",
        help_text="Les catégories auxquelles ces graines appartiennent.",
    )
    description = models.TextField(
        blank=True, help_text="Une description détaillée des graines (facultatif)."
    )
    quantity = models.PositiveIntegerField(
        help_text="La quantité disponible de ces graines."
    )
    status = models.CharField(
        max_length=10,
        choices=Status.STATUS.choices,
        help_text="Le statut actuel des graines.",
    )
    price_per_kilo = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Le prix des graines au kilogramme."
    )
    article_code = models.CharField(
        max_length=150,
        help_text="Code de l'article de la graine.",
    )
    scientific_name = models.CharField(
        max_length=150,
        help_text="Nom scientifique de la graine.",
    )
    species_code = models.CharField(
        max_length=150,
        help_text="Code de l'espèce de la graine.",
    )
    poids = models.PositiveIntegerField(
        default=9,
        help_text="1 = très important, 9 = peu important"
    )

    def __str__(self):
        return f"{self.name}"
