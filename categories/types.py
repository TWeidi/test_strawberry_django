# from django.db.models import Exists, OuterRef, Prefetch
from strawberry import auto, relay
from strawberry_django import connection, filter, type
from strawberry_django.relay import ListConnectionWithTotalCount

from . import models


@type(models.ContentType)
class ContentType(relay.Node):
    app_label: auto
    model: auto


@type(models.Category)
class Category(relay.Node):
    name: auto
    description: auto
    content_type: ContentType


@type(models.Tag)
class Tag(relay.Node):
    category: Category
    name: auto
    description: auto


@type
class CategoryQueries:
    """All available queries for this app."""
    content_types: ListConnectionWithTotalCount[ContentType] = connection()
    categories: ListConnectionWithTotalCount[Category] = connection()
    tags: ListConnectionWithTotalCount[Tag] = connection()
