import contextlib

from django.apps import AppConfig


class PlantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sngf_api.plant"

    def ready(self):
        with contextlib.suppress(ImportError):
            import sngf_api.plant.signals
