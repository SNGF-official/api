from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Category

DEFAULT_CATEGORIES = [
    ("AGROFORESTIERES", "Agroforestières"),
    ("ENDEMIQUES_AUTOCHTONES", "Endémiques autochtones"),
    ("EXOTIQUES_REBOISEMENT", "Exotiques de reboisement"),
    ("ORNEMENTALES", "Ornementales"),
    ("EMBROUSSAILLEMENTS", "Embrousseillements"),
]


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    for code, display_name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            name=code,
            defaults={"display_name": display_name}
        )
