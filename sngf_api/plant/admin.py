from django.contrib import admin
from django.utils.html import format_html

from .models import Plant
from .models import PlantImage
from .models import Seed


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1
    readonly_fields = ["preview"]

    @admin.display(description="Aperçu")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Aucune image"


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status", "size", "quantity")
    search_fields = ("name", "category")
    list_filter = ("category", "status", "size")
    inlines = [PlantImageInline]
    fieldsets = (
        (None, {"fields": ("name", "category", "description", "status", "quantity")}),
        ("Taille & Prix", {"fields": ("size", "prices")}),
    )


@admin.register(Seed)
class SeedAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status", "price_per_kilo", "quantity")
    search_fields = ("name", "category")
    list_filter = ("category", "status")


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text", "image_preview")
    readonly_fields = ("image_preview",)
    search_fields = ("product__name", "alt_text")

    @admin.display(description="Aperçu")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Pas d'image"
