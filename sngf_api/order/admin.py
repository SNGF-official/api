from django.contrib import admin

from .models import Order
from .models import OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ["plant"]
    can_delete = False
    show_change_link = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "customer_email", "number", "status", "submitted_at"]
    list_filter = ["status", "submitted_at"]
    search_fields = ["id", "name", "customer_email"]
    readonly_fields = ["created_at", "updated_at", "submitted_at"]
    ordering = ["-submitted_at"]
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {"fields": ("name", "customer_email", "status", "number")}),
        (
            "Infos supplémentaires",
            {
                "fields": ("submitted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
