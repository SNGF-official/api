from django.contrib import admin
from django.contrib import messages

from .models import Order
from .models import OrderItem
from .utils import send_order_confirmation_email


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "contact_name",
        "contact_email",
        "contact_number",
        "status",
        "submitted_at",
        "get_items_count",
    )
    list_filter = ("status", "submitted_at")
    search_fields = ("contact_name", "contact_email")
    ordering = ("-submitted_at",)
    readonly_fields = ("id", "submitted_at")
    inlines = [OrderItemInline]

    @admin.display(description="Nombre d'items")
    def get_items_count(self, obj):
        """Méthode pour afficher le nombre d'items dans chaque commande"""
        return obj.items.count()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_id", "type", "quantity", "unit", "size", "price")
    list_filter = ("type", "unit")
    search_fields = ("product_id", "order__contact_name")
    ordering = ("order", "product_id")
    readonly_fields = ("order", "product_id")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "contact_name", "contact_email", "submitted_at", "status")
    actions = ["resend_confirmation_email"]

    @admin.action(description="📨 Renvoyer l'email de confirmation")
    def resend_confirmation_email(self, request, queryset):
        sent = 0
        for order in queryset:
            try:
                send_order_confirmation_email(order)
                sent += 1
            except Exception as e:
                self.message_user(
                    request,
                    f"Erreur lors de l'envoi pour la commande {order.id} : {str(e)}",
                    level=messages.ERROR,
                )
        if sent:
            self.message_user(request, f"{sent} email(s) de confirmation renvoyé(s).")
