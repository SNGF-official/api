from django.contrib import admin

from .models import Category
from .models import Plant
from .models import PlantImage
from .models import PlantSizePrice
from .models import Seed
from .models import SeedImage
from django.contrib.admin import SimpleListFilter


class HasPlantImageFilter(SimpleListFilter):
    title = "Image"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return [
            ("yes", "✅ Avec image"),
            ("no", "❌ Sans image"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(images__isnull=False).distinct()
        elif self.value() == "no":
            return queryset.filter(images__isnull=True)
        return queryset


class HasSeedImageFilter(SimpleListFilter):
    title = "Image"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return [
            ("yes", "✅ Avec image"),
            ("no", "❌ Sans image"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(images__isnull=False).distinct()
        elif self.value() == "no":
            return queryset.filter(images__isnull=True)
        return queryset

class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1


class PlantSizePriceInline(admin.TabularInline):
    model = PlantSizePrice
    extra = 1


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "status", "image")
    list_filter = ("categories", "status", HasPlantImageFilter)
    search_fields = ("name", "description")
    inlines = [PlantImageInline, PlantSizePriceInline]
    filter_horizontal = ("categories",)
    ordering = ("name",)

    def image(self, obj):
        return "✅" if obj.images.exists() else "❌"

    image.short_description = "Image"
    image.admin_order_field = None



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
    list_display = ("name", "quantity", "status", "price_per_kilo", "image")
    list_filter = ("categories", "status", HasSeedImageFilter)
    search_fields = ("name", "description")
    inlines = [SeedImageInline]
    filter_horizontal = ("categories",)
    ordering = ("name",)

    def image(self, obj):
        return "✅" if obj.images.exists() else "❌"

    image.short_description = "Image"
    image.admin_order_field = None



@admin.register(SeedImage)
class SeedImageAdmin(admin.ModelAdmin):
    list_display = ("seed", "alt_text", "image")
    list_filter = ("seed",)
    search_fields = ("alt_text",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name")
    search_fields = ("name", "display_name")
    ordering = ("name",)
