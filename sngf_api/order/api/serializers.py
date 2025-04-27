from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sngf_api.order.models import Order
from sngf_api.order.models import OrderItem


class OrderItemSerializer(ModelSerializer):
    productId = serializers.IntegerField()  # noqa: N815
    type = serializers.ChoiceField(choices=["PLANT", "SEED"])
    quantity = serializers.IntegerField()
    unit = serializers.CharField(allow_null=True, required=False)
    size = serializers.CharField(allow_null=True, required=False)
    price = serializers.FloatField(allow_null=True, required=False)

    class Meta:
        model = OrderItem
        fields = ["productId", "type", "quantity", "unit", "size", "price"]


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "submitted_at",
            "status",
            "items",
            "contact_name",
            "contact_email",
            "contact_number",
        ]
        read_only_fields = ["id", "submitted_at", "items"]


class OrderCreateSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["status", "items", "contact_name", "contact_email", "contact_number"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])

        order = Order.objects.create(
            status=validated_data.get("status"),
            contact_name=validated_data.get("contact_name"),
            contact_email=validated_data.get("contact_email"),
            contact_number=validated_data.get("contact_number"),
        )

        for item_data in items_data:
            product_id = item_data.get("productId")
            quantity = item_data.get("quantity", 1)
            item_type = item_data.get("type", "PLANT")
            unit = item_data.get("unit", "")
            size = item_data.get("size", "")
            price = item_data.get("price", 0.00)

            if product_id is None:
                msg = "Le champ 'productId' est obligatoire."
                raise serializers.ValidationError(msg)

            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=quantity,
                type=item_type,
                unit=unit,
                size=size,
                price=price,
            )

        return order
