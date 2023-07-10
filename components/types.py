from typing import Optional

from strawberry import auto, relay
from strawberry_django import connection, filter, type
from strawberry_django.relay import ListConnectionWithTotalCount

from components import models

type(models.UserModel)
class Profile(relay.Node):
    first_name: auto
    last_name: auto
    username: auto
    email: auto


type(models.Company)
class Company(relay.Node):
    name: auto
    url: auto


@type(models.Type)
class Type(relay.Node):
    name: auto
    full_name: auto
    description: auto


@type(models.FNode)
class FNode(relay.Node):
    path: auto
    ref: auto


@type(models.Library)
class Library(relay.Node):
    path: auto
    ref: auto


@type(models.LifecycleState)
class LifecycleState(relay.Node):
    name: auto
    full_name: auto
    description: auto


@type(models.Link)
class Link(relay.Node):
    name: auto
    url: auto


@type(models.MountingType)
class MountingType(relay.Node):
    name: auto
    full_name: auto
    description: auto


@type(models.Qualification)
class Qualification(relay.Node):
    name: auto
    full_name: auto
    description: auto


@type(models.AnnotatedQualification)
class AnnotatedQualification(relay.Node):
    annotation: auto
    component: 'Component'
    qualification: Qualification


@type(models.Review)
class Review(relay.Node):
    annotated_qualification: AnnotatedQualification
    component: 'Component'
    date: auto
    reviewer: Profile


@type(models.Package)
class Package(relay.Node):
    name: auto
    description: auto


@type(models.BaseComponent)
class BaseComponent(relay.Node):
    type: Type
    autogenerate_description: auto
    autogenerate_value: auto
    description: auto
    f_nodes: ListConnectionWithTotalCount[FNode] = connection()
    library: Library
    links: ListConnectionWithTotalCount[Link] = connection()
    value: auto

@filter(models.Component, lookups=True)
class ComponentFilter:
    description: auto
    type: auto


@type(models.Component, filters=ComponentFilter)
class Component(relay.Node):
    type: Type
    autogenerate_description: auto
    autogenerate_value: auto
    creator: Profile
    created: auto
    description: auto
    f_nodes: ListConnectionWithTotalCount[FNode] = connection(prefetch_related=['f_nodes'])
    last_modified: auto
    last_modifier: Profile
    library: Library
    lifecycle_state: LifecycleState
    links: ListConnectionWithTotalCount[Link] = connection(prefetch_related=['links'])
    manufacturer: Company
    mpn: auto
    mounting: MountingType
    package: Optional[Package]
    remarks: auto
    reviews: ListConnectionWithTotalCount[Review] = connection(prefetch_related=['reviews'])
    stock: auto
    qualifications: ListConnectionWithTotalCount[Qualification] = connection(prefetch_related=['qualifications'])
    value: auto
    x: auto
    y: auto
    z: auto


@type
class ComponentQueries:
    """All available queries for this app."""
    node: Optional[relay.Node] = relay.node()

    types: ListConnectionWithTotalCount[Type] = connection()
    base_components: ListConnectionWithTotalCount[BaseComponent] = connection()
    components: ListConnectionWithTotalCount[Component] = connection()
    links: ListConnectionWithTotalCount[Link] = connection()