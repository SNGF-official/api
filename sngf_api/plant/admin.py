from django.contrib import admin

from .models import Category
from .models import Plant
from .models import PlantImage
from .models import PlantSizePrice
from .models import Seed
from .models import SeedImage


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1


class PlantSizePriceInline(admin.TabularInline):
    model = PlantSizePrice
    extra = 1


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "status")
    list_filter = ("categories", "status")
    search_fields = ("name", "description")
    inlines = [PlantImageInline, PlantSizePriceInline]
    filter_horizontal = ("categories",)


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ("plant", "alt_text", "image")
    list_filter = ("plant",)
    search_fields = ("alt_text",)


@admin.register(PlantSizePrice)
class PlantSizePriceAdmin(admin.ModelAdmin):
    list_display = ("plant", "size", "price")
    list_filter = ("plant", "size")
    search_fields = ("plant__name",)


class SeedImageInline(admin.TabularInline):
    model = SeedImage
    extra = 1


@admin.register(Seed)
class SeedAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "status", "price_per_kilo")
    list_filter = ("categories", "status")
    search_fields = ("name", "description")
    inlines = [SeedImageInline]
    filter_horizontal = ("categories",)


@admin.register(SeedImage)
class SeedImageAdmin(admin.ModelAdmin):
    list_display = ("seed", "alt_text", "image")
    list_filter = ("seed",)
    search_fields = ("alt_text",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name")
    search_fields = ("name", "display_name")
