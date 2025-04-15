from rest_framework import serializers

from sngf_api.plant.models import Plant
from sngf_api.plant.models import PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    image_urls = serializers.ImageField(required=False, source="image")

    class Meta:
        model = PlantImage
        fields = ["id", "image_urls", "alt_text"]
        read_only_fields = ["id"]


class PlantListSerializer(serializers.ModelSerializer):
    image_urls = PlantImageSerializer(many=True, read_only=True, source="images")

    class Meta:
        model = Plant
        fields = [
            "id",
            "name",
            "category",
            "type",
            "description",
            "price",
            "price_per_unit",
            "unit",
            "quantity",
            "size",
            "status",
            "image_urls",
        ]


class PlantDetailSerializer(serializers.ModelSerializer):
    image_urls = PlantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"
        read_only_fields = ["id"]
