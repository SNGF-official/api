from rest_framework import serializers

from sngf_api.plant.models import Plant
from sngf_api.plant.models import PlantImage
from sngf_api.plant.models import PlantSizePrice


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ["id", "alt_text", "image"]
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
