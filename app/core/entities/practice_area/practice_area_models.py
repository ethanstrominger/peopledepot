from django.db import models
from core.models import AbstractBaseModel


class PracticeArea(AbstractBaseModel):
    """
    Practice Area
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}"
