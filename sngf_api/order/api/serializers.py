from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from sngf_api.core.mail import SendMail
from sngf_api.order.models import Order
from sngf_api.order.models import OrderItem
from django.utils.timezone import now

from sngf_api.plant.models import Seed, Plant


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
    status = serializers.ChoiceField(
        choices=Order.OrderStatus.choices,
        default=Order.OrderStatus.PENDING,
        required=False,
    )
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
            status=validated_data.get("status", Order.OrderStatus.PENDING),
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
        now_dt = now().strftime("%d/%m/%Y %H:%M")
        items = []
        for item in order.items.all():
            if item.type == "SEED":
                try:
                    seed = Seed.objects.get(id=item.product_id)
                    item.seed = seed
                except Seed.DoesNotExist:
                    item.seed = None
            else:
                try:
                    plant = Plant.objects.get(id=item.product_id)
                    item.plant = plant
                except Plant.DoesNotExist:
                    item.plant = None
            items.append(item)
        total_order_amount = sum(
            float(item.price) * int(item.quantity)
            for item in items
            if float(item.price) is not None and int(item.quantity) is not None
        )
        plain_lines = []
        for item in items:
            if item.type == "SEED":
                product_name = getattr(item.seed, "scientific_name", "Graine inconnue")
                price = f"{item.seed.price_per_kilo:.0f} Ar/kg" if item.seed and item.seed.price_per_kilo else "Prix inconnu"
                size_label = "-"  # non applicable
            else:
                product_name = getattr(item.plant, "scientific_name", "Plante inconnue")
                size_map = {
                    "PM": "Petit modèle",
                    "MM": "Modèle moyen",
                    "GM": "Grand modèle",
                    "X": "Extrème modèle",
                    "UN": "Modèle unique",
                }
                size_label = size_map.get(item.size, item.size or "-")
                price = f"{item.price:.0f} Ar"

            total_price = item.price * item.quantity
            line = (
                f"- Produit : {product_name} | "
                f"Type : {'Graine' if item.type == 'SEED' else 'Plante'} | "
                f"Quantité : {item.quantity} {item.unit or ''} | "
                f"Taille : {size_label} | "
                f"Prix unitaire : {price} | "
                f"Total : {total_price:.0f} Ar"
            )
            plain_lines.append(line)

        plain_body = f"""
        Nouvelle commande reçue le {now_dt}

        Client :
        - Nom : {order.contact_name}
        - Email : {order.contact_email}
        - Téléphone : {order.contact_number}

        Commande :
        {chr(10).join(plain_lines)}

        Merci de vérifier dans l'administration de SNGF.
        """

        html_body = render_to_string("email/order_confirmation.html", {
            "order": order,
            "items": items,
            "now": now_dt,
            "total": f"{total_order_amount:.2f}",
        })

        admin_emails = settings.ORDER_NOTIFICATION_EMAILS
        from_email = order.contact_email or settings.DEFAULT_FROM_EMAIL
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body.strip(),
            from_email=from_email,
            to=admin_emails,
        )
        email.attach_alternative(html_body, "text/html")
        email.send()

        return order
