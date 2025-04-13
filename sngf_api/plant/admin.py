from django.contrib import admin

from .models import Plant
from .models import PlantImage


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    inlines = [PlantImageInline]
    list_display = ("name", "category", "price", "quantity", "status")
    list_filter = ("category", "size", "status")
    search_fields = ("name", "description")
