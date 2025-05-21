from django.db import models

from sngf_api.core.models import BaseModel
from sngf_api.core.models import Contactable


class Contact(BaseModel, Contactable):
    message = models.TextField()

    def __str__(self):
        return f"Message de {self.name or 'Anonyme'}"
