from rest_framework import serializers

from sngf_api.event.models import EventModel

# ruff : noqa : N815


class EventSerializer(serializers.ModelSerializer):
    imageUrl = serializers.ImageField(source="image")

    class Meta:
        model = EventModel
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "imageUrl",
            "status",
        ]
