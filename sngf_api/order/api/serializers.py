from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sngf_api.core.mail import SendMail
from sngf_api.order.models import Order
from sngf_api.order.models import OrderItem


class OrderItemSerializer(ModelSerializer):
    productId = serializers.UUIDField(source="product_id")  # noqa: N815

    class Meta:
        model = OrderItem
        fields = ["productId", "type", "quantity", "unit", "size", "price"]


class OrderCreateItemSerializer(ModelSerializer):
    product_id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=["PLANT", "SEED"])
    quantity = serializers.IntegerField()
    unit = serializers.CharField(allow_null=True, required=False)
    size = serializers.CharField(allow_null=True, required=False)
    price = serializers.FloatField(allow_null=True, required=False)

    class Meta:
        model = OrderItem
        fields = ["product_id", "type", "quantity", "unit", "size", "price"]


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
    status = serializers.CharField(required=False, default="PENDING")
    class Meta:
        model = Order
        fields = [
            "status",
            "items",
            "contact_name",
            "contact_email",
            "contact_number",
            "submitted_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])

        order = Order.objects.create(
            status=validated_data.get("status"),
            contact_name=validated_data.get("contact_name"),
            contact_email=validated_data.get("contact_email"),
            contact_number=validated_data.get("contact_number"),
        )

        for item_data in items_data:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity", 1)
            item_type = item_data.get("type", "PLANT")
            unit = item_data.get("unit", "")
            size = item_data.get("size", "")
            price = item_data.get("price", 0.00)

            if product_id is None:
                msg = "Le champ 'productId' est obligatoire."
                raise serializers.ValidationError(msg)

            existing_item = OrderItem.objects.filter(
                order=order, product_id=product_id, type=item_type, size=size
            ).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                OrderItem.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=quantity,
                    type=item_type,
                    unit=unit,
                    size=size,
                    price=price,
                )

        subject = f"Nouvelle commande au nom de #{order.contact_name}"

        item_lines = []
        for item in order.items.all():
            line = (
                f"- Produit ID: {item.product_id} | "
                f"Type: {item.type} | "
                f"Quantité: {item.quantity} {item.unit or ''} | "
                f"Taille: {item.size or '-'} | "
                f"Prix unitaire: {item.price:.2f}€"
            )
            item_lines.append(line)
        items_text = "\n".join(item_lines)

        body = f"""
        Nouvelle commande soumise :
            Informations client :
            - Nom : {order.contact_name}
            - Email : {order.contact_email}
            - Téléphone : {order.contact_number}

        Détails de la commande :
            {items_text}
        Merci de vérifier dans l'admin.
                """
        admin_emails = settings.ORDER_NOTIFICATION_EMAILS
        from_email = order.contact_email or "no-reply@example.com"

        mail = SendMail(
            subject=subject,
            body=body,
            to=admin_emails,
            from_email=from_email,
        )
        mail.send()

        return order
