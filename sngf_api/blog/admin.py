from django.contrib import admin

from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "status")
    list_filter = ("status", "published_at")
    search_fields = ("title", "description")
    ordering = ("-published_at",)
