from django.contrib import admin

from sngf_api.files.models import FileModel


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "created_at", "updated_at")
    search_fields = ("name", "type")
    list_filter = ("type", "created_at")
    readonly_fields = ("created_at", "updated_at")
