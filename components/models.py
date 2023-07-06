from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from ordered_model.models import OrderedModel

UserModel = get_user_model()


def pluralize(noun):
    if noun[-1] == 'y':
        return noun[:-1] + 'ies'
    elif noun[-2:] == 'ch':
        return noun + 'es'
    elif noun[-1] == "s":
        return noun
    else:
        return noun + 's'


class NameDescriptionMixin(models.Model):
    """NameDescriptionMixin adds a name and a description field to a model."""
    name = models.CharField(max_length=256, default='MyName', unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class EnumMixin(NameDescriptionMixin, models.Model):
    full_name = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True


class WebEntityMixin(models.Model):
    name = models.CharField(max_length=256, default='MyName')
    url = models.CharField(max_length=256, validators=[MinLengthValidator(1)])

    class Meta:
        abstract = True

    def __init_subclass__(cls) -> None:
        cls._meta.constraints = [
            models.UniqueConstraint(fields=['name', 'url'], name="unique-name-url")
        ]
        return super().__init_subclass__()


class CreatorMixin(models.Model):
    """CreatorMixin adds a reference to the user that created the instance and the creation date."""
    creator = models.ForeignKey(UserModel, on_delete=models.PROTECT, editable=True)
    created = models.DateTimeField(editable=False, blank=True)

    def __init_subclass__(cls) -> None:
        cls.creator.field.remote_field.related_name = f"created_{pluralize(cls.__name__.lower())}"
        return super().__init_subclass__()

    class Meta:
        abstract = True
        ordering = ['-created']

    def save(self, *args, **kwargs) -> None:
        # On save, update timestamps
        if not self.pk and not self.created:
            self.created = timezone.now()
        return super().save(*args, **kwargs)


class ModifiedMixin(models.Model):
    """ModifiedMixin adds the date of the last modification to a model instance and the user that modified it."""
    last_modifier = models.ForeignKey(UserModel, on_delete=models.PROTECT,
                                      editable=True)
    last_modified = models.DateTimeField(editable=False, blank=True)

    def __init_subclass__(cls) -> None:
        cls.last_modifier.field.remote_field.related_name = f"modified_{pluralize(cls.__name__.lower())}"
        return super().__init_subclass__()

    class Meta:
        abstract = True
        ordering = ['-last_modified']

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if self.pk or (not self.pk and not self.last_modified):
            self.last_modified = timezone.now()

        return super().save(*args, **kwargs)


class Company(WebEntityMixin, models.Model):
    ...


class LifecycleState(EnumMixin, models.Model):
    ...


class Link(WebEntityMixin, models.Model):
    ...


class Library(models.Model):
    ref = models.CharField(max_length=256, unique=True)
    path = models.CharField(max_length=128, default="Some Librabry")


class MountingType(EnumMixin, models.Model):
    ...


class FNode(models.Model):
    ref = models.CharField(max_length=256, unique=True)
    path = models.CharField(max_length=128, default="Some FNode")


class Package(NameDescriptionMixin, models.Model):
    ...


class Qualification(EnumMixin, models.Model):
    ...


class Type(EnumMixin, models.Model):
    ...


class Review(models.Model):
    annotated_qualification = models.ForeignKey(
        'AnnotatedQualification', on_delete=models.CASCADE, related_name="reviews",
        null=True, blank=True
    )
    component = models.ForeignKey(
        'Component', on_delete=models.CASCADE, related_name="reviews", null=True, 
        blank=True)
    date = models.DateTimeField(editable=False, blank=True)
    reviewer = models.ForeignKey(UserModel, on_delete=models.PROTECT, 
                                 related_name='reviews')

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.pk and not self.date:
            self.date = timezone.now()
        return super().save(*args, **kwargs)


class BaseComponent(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="components")
    autogenerate_description = models.BooleanField(default=True, blank=True)
    autogenerate_value = models.BooleanField(default=True, blank=True)
    description = models.TextField(null=True, blank=True)
    f_nodes = models.ManyToManyField(FNode, through='OrderedFNode', 
                                     related_name="components", blank=True)
    library = models.ForeignKey(Library, on_delete=models.PROTECT, 
                                related_name="components")
    links = models.ManyToManyField(Link, through='OrderedLink', blank=True,
                                   related_name="components")
    value = models.CharField(max_length=256, unique=False, null=True, blank=True)


class Component(BaseComponent, CreatorMixin, ModifiedMixin, models.Model):
    lifecycle_state = models.ForeignKey(LifecycleState, on_delete=models.PROTECT, 
                                        related_name="components")
    manufacturer = models.ForeignKey(Company, on_delete=models.PROTECT, 
                                     related_name="components")
    mpn = models.CharField(max_length=64)
    mounting = models.ForeignKey(MountingType, on_delete=models.PROTECT,
                                 related_name="components")
    package = models.ForeignKey(Package, null=True, blank=True, 
                                on_delete=models.PROTECT,
                                related_name="components")
    qualifications = models.ManyToManyField(Qualification, blank=True, 
                                            related_name="components",
                                            through="AnnotatedQualification")
    remarks = models.CharField(max_length=1024, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    z = models.FloatField(null=True, blank=True)


class OrderedFNode(OrderedModel):
    f_node = models.ForeignKey(FNode, on_delete=models.PROTECT, related_name="positions")
    base_component = models.ForeignKey(BaseComponent, on_delete=models.CASCADE, 
                                       related_name="ordered_f_nodes")
    order_with_respect_to = 'base_component'

    @property
    def position(self):
        return f'FNode Ref{" " + self.order if self.order != 0 else ""}'


class OrderedLink(OrderedModel):
    link = models.ForeignKey(Link, on_delete=models.PROTECT, related_name="positions")
    base_component = models.ForeignKey(BaseComponent, on_delete=models.CASCADE,
                                       related_name="ordered_links")
    order_with_respect_to = 'base_component'

    @property
    def position(self) -> str:
        return f'Link{" " + self.order if self.order != 0 else ""}'


class AnnotatedQualification(models.Model):
    annotation = models.TextField(blank=True, null=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE,
                                  related_name="annotated_qualifications")
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT,
                                      related_name="annotations")
