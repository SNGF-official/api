from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from sngf_api.contact.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    number = PhoneNumberField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Contact
        fields = ["id", "name", "number", "customer_email", "message", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        customer_email = data.get("customer_email")
        number = data.get("number")

        if not customer_email and not number:
            raise serializers.ValidationError(
                "Veuillez renseigner au moins un numéro de téléphone ou une adresse email."
            )

        return data
