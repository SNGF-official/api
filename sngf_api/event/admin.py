from django.contrib import admin

from .models import EventModel


@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "status")
    search_fields = ("title", "description", "location")
    list_filter = ("status", "date")
    ordering = ("-date",)
