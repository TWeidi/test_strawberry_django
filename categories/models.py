"""Category models."""
from django.contrib.contenttypes.models import ContentType
from django.db import models

from components.models import NameDescriptionMixin


class Category(NameDescriptionMixin, models.Model):
    name = models.CharField(max_length=256)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'content_type'], name="unique-model-category")
        ]


class Tag(NameDescriptionMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tags')
