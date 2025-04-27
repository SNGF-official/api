from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sngf_api.order.models import Order
from sngf_api.order.models import OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "type", "quantity", "unit", "size", "price"]


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
    items = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Order
        fields = ["status", "items", "contact_name", "contact_email", "contact_number"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        instance.status = validated_data.get("status", instance.status)
        instance.contact_name = validated_data.get(
            "contact_name", instance.contact_name
        )
        instance.contact_email = validated_data.get(
            "contact_email", instance.contact_email
        )
        instance.contact_number = validated_data.get(
            "contact_number", instance.contact_number
        )
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance
