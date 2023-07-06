from typing import Optional

import strawberry
import strawberry.django
from strawberry.schema.config import StrawberryConfig

from strawberry_django_plus import gql
from strawberry_django_plus.directives import SchemaDirectiveExtension
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from .types import Type, BaseComponent, Component, Link


@gql.type
class Query:
    """All available queries for this schema."""
    node: Optional[gql.Node] = gql.django.node()

    types: gql.django.ListConnectionWithTotalCount[Type] = gql.django.connection()
    base_components: gql.django.ListConnectionWithTotalCount[BaseComponent] = gql.django.connection()
    components: gql.django.ListConnectionWithTotalCount[Component] = gql.django.connection()
    links: gql.django.ListConnectionWithTotalCount[Link] = gql.django.connection()

schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(relay_max_results=1000),
    extensions=[
        SchemaDirectiveExtension,
        DjangoOptimizerExtension
    ]
)
