from typing import Optional

from strawberry import relay
from strawberry_django_plus import gql

from components import models

@gql.django.type(models.UserModel)
class Profile(relay.Node):
    first_name: gql.auto
    last_name: gql.auto
    username: gql.auto
    email: gql.auto


@gql.django.type(models.Company)
class Company(relay.Node):
    name: gql.auto
    url: gql.auto


@gql.django.type(models.Type)
class Type(relay.Node):
    name: gql.auto
    full_name: gql.auto
    description: gql.auto


@gql.django.type(models.FNode)
class FNode(relay.Node):
    path: gql.auto
    ref: gql.auto


@gql.django.type(models.Library)
class Library(relay.Node):
    path: gql.auto
    ref: gql.auto


@gql.django.type(models.LifecycleState)
class LifecycleState(relay.Node):
    name: gql.auto
    full_name: gql.auto
    description: gql.auto


@gql.django.type(models.Link)
class Link(relay.Node):
    name: gql.auto
    url: gql.auto


@gql.django.type(models.MountingType)
class MountingType(relay.Node):
    name: gql.auto
    full_name: gql.auto
    description: gql.auto


@gql.django.type(models.Qualification)
class Qualification(relay.Node):
    name: gql.auto
    full_name: gql.auto
    description: gql.auto


@gql.django.type(models.AnnotatedQualification)
class AnnotatedQualification(relay.Node):
    annotation: gql.auto
    component: 'Component'
    qualification: Qualification


@gql.django.type(models.Review)
class Review(relay.Node):
    annotated_qualification: AnnotatedQualification
    component: 'Component'
    date: gql.auto
    reviewer: Profile


@gql.django.type(models.Package)
class Package(relay.Node):
    name: gql.auto
    description: gql.auto


@gql.django.type(models.BaseComponent)
class BaseComponent(relay.Node):
    type: Type
    autogenerate_description: gql.auto
    autogenerate_value: gql.auto
    description: gql.auto
    f_nodes: gql.django.ListConnectionWithTotalCount[FNode] = gql.django.connection()
    library: Library
    links: gql.django.ListConnectionWithTotalCount[Link] = gql.django.connection()
    value: gql.auto

@gql.django.filter(models.Component, lookups=True)
class ComponentFilter:
    description: gql.auto
    type: gql.auto


@gql.django.type(models.Component, filters=ComponentFilter)
class Component(relay.Node):
    type: Type
    autogenerate_description: gql.auto
    autogenerate_value: gql.auto
    creator: Profile
    created: gql.auto
    description: gql.auto
    f_nodes: gql.django.ListConnectionWithTotalCount[FNode] = gql.django.connection(prefetch_related=['f_nodes'])
    last_modified: gql.auto
    last_modifier: Profile
    library: Library
    lifecycle_state: LifecycleState
    links: gql.django.ListConnectionWithTotalCount[Link] = gql.django.connection(prefetch_related=['links'])
    manufacturer: Company
    mpn: gql.auto
    mounting: MountingType
    package: Optional[Package]
    remarks: gql.auto
    reviews: gql.django.ListConnectionWithTotalCount[Review] = gql.django.connection(prefetch_related=['reviews'])
    stock: gql.auto
    qualifications: gql.django.ListConnectionWithTotalCount[Qualification] = gql.django.connection(prefetch_related=['qualifications'])
    value: gql.auto
    x: gql.auto
    y: gql.auto
    z: gql.auto
