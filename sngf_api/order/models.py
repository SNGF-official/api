from django.db import models

from sngf_api.core.models import BaseModel
from sngf_api.core.models import Contactable
from sngf_api.plant.models import Plant


class Order(BaseModel, Contactable):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmée"
        CANCELLED = "CANCELLED", "Annulée"

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
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("order", "plant")

    def __str__(self):
        return f"{self.quantity} x {self.plant.name} (Commande {self.order.id})"
