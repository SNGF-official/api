from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "customer_email", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "customer_email", "message"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    fieldsets = (
        (None, {"fields": ("name", "customer_email")}),
        ("Message", {"fields": ("message",)}),
        (
            "Meta",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
