from rest_framework import serializers

from sngf_api.event.models import EventModel


class EventSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(required=False, source="image")

    class Meta:
        model = EventModel
        fields = [
            "id",
            "title",
            "description",
            "status",
            "date",
            "location",
            "image_url",
        ]
