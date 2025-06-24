from rest_framework import serializers

from sngf_api.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "number", "customer_email", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
