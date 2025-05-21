from uuid import uuid4

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from sngf_api.core.models import BaseModel


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmée"
        CANCELLED = "CANCELLED", "Annulée"

    contact_name = models.CharField(  # noqa: DJ001
        max_length=255, null=True, blank=True
    )  # Rendre nullable
    contact_email = models.EmailField(null=True, blank=True)  # noqa: DJ001
    contact_number = PhoneNumberField(null=True, blank=True)  # Rendre nullable
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    def __str__(self):
        return f"Commande {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_id = models.UUIDField(default=uuid4())
    type = models.CharField(max_length=100, default="")
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=10, blank=True)  # 'unit' or 'kg'
    size = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ("order", "product_id", "type", "size")

    def __str__(self):
        return (
            f"{self.quantity} x (Type: {self.type}, ID: {self.product_id})"
            f"(Commande {self.order.id})"
        )
