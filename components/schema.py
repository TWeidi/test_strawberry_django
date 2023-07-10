from typing import Optional

from strawberry import Schema, relay, tools, type
from strawberry.django import connection
from strawberry.schema.config import StrawberryConfig
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django.relay import ListConnectionWithTotalCount

from .types import ComponentQueries
from categories.types import CategoryQueries


Query = tools.merge_types("FullQuery", (CategoryQueries, ComponentQueries))
    

schema = Schema(
    query=Query,
    config=StrawberryConfig(relay_max_results=1000),
    extensions=[
        DjangoOptimizerExtension
    ]
)
