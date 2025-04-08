from django.db import models


class DummyModel(models.Model):
    """
    Used for test
    """

    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
