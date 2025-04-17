from rest_framework import serializers

from sngf_api.plant.models import Plant
from sngf_api.plant.models import PlantImage
from sngf_api.plant.models import PlantSizePrice
from sngf_api.plant.models import Seed
from sngf_api.plant.models import SeedImage

# ruff : noqa: N815


class ImageSerializer(serializers.ModelSerializer):
    altText = serializers.CharField(source="alt_text")

    class Meta:
        model = PlantImage
        fields = ["id", "altText", "image"]
        read_only_fields = ["id"]


class ImageSeedSerializer(serializers.ModelSerializer):
    altText = serializers.CharField(source="alt_text")

    class Meta:
        model = SeedImage
        fields = ["id", "altText", "image"]
        read_only_fields = ["id"]


class PlantSizePriceSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source="get_size_display")

    class Meta:
        model = PlantSizePrice
        fields = ["size", "price"]


class PlantSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    prices = PlantSizePriceSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = [
            "id",
            "name",
            "category",
            "description",
            "quantity",
            "status",
            "images",
            "prices",
        ]
        read_only_fields = ["id", "images", "prices"]


class SeedSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    pricePerKilo = serializers.DecimalField(
        source="price_per_kilo", max_digits=10, decimal_places=2
    )

    class Meta:
        model = Seed
        fields = [
            "id",
            "name",
            "category",
            "description",
            "quantity",
            "status",
            "images",
            "pricePerKilo",
        ]
        read_only_fields = ["id", "images"]
