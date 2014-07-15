# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django_autocomplete.meta import AutocompleteMeta


API_FILTER_PATH = 'api/filter'


class Autocomplete(object):

  @property
  def autocomplete(self):
      name = self.__class__.__name__.lower()
      return AutocompleteMeta(
          name=name,
          path='%s/%s' % (API_FILTER_PATH, name),
          permissions=True
          )


class Timestamped(models.Model):
    """
    The Timestamped model, all models in the application share its attributes.

        >>> obj = Timestamped()
        >>> obj.created

    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Base(models.Model, Autocomplete):
    """
    The Base model, all models in the application share its attributes.

        >>> obj = Base(name='base')
        >>> obj.name
        'base'

    """
    name = models.CharField(
        max_length=30
        )

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.name)

    def __str__(self):
        return '%s' % (self.name)


class Documentation(Base, Timestamped):
    """
    The Documentation model.

        >>> obj = Documentation.objects.create(name='usa')
        >>> obj.autocomplete.name
        'documentation'
        >>> obj.autocomplete.path
        'api/filter/documentation'

        >>> obj.delete()

    """
    class Meta:
        verbose_name_plural = 'Documentation'


class HasDoc(models.Model):
    """
    Abstract model class to store documentation to models

    Other classes are expected to subclass this model to contain documents.::

        class ModelHasDocs(HasDocumentation)
            pass

    """
    documentation = models.ManyToManyField(
        Documentation,
        blank=True, null=True,
        related_name="documentation_for_%(class)s"
        )

    class Meta:
        abstract = True


class Country(Base, HasDoc, Timestamped):
    """
    The Country model. Each town has a ForeignKey to its Country.

        >>> obj = Country.objects.create(name='usa')
        >>> obj.autocomplete.name
        'country'
        >>> obj.autocomplete.path
        'api/filter/country'

        >>> obj.delete()

    """
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Organisation(Base, HasDoc, Timestamped):
    """
    The Organisation model. It has a many to many relationship with Towns.

        >>> obj = Organisation.objects.create(name='microsoft')
        >>> obj.autocomplete.name
        'organisation'
        >>> obj.autocomplete.path
        'api/filter/organisation'

    Has docs:

        >>> obj.documentation.all()
        []

        >>> obj.delete()

    """
    class Meta:
        verbose_name = 'Organisation'


class Town(Base, HasDoc, Timestamped):
    """
    The Town model.

        >>> usa = Country.objects.create(name='usa')
        >>> obj = Town.objects.create(name='redmond', country=usa)
        >>> obj.autocomplete.name
        'town'
        >>> obj.autocomplete.path
        'api/filter/town'

    Has a country:

        >>> obj.country
        <Country: usa>

    Has organisations:

        >>> obj.organisations.all()
        []

    Can have sister towns:

        >>> obj.sister_towns.add(Town.objects.create(name='redmond', country=usa))
        >>> obj.sister_towns.all()
        [<Town: redmond>]

    Clean up

        >>> usa.delete()
        >>> obj.delete()

    """
    country = models.ForeignKey(Country, null=True)
    organisations = models.ManyToManyField(
        Organisation,
        through='project.OrganisationTown',
        related_name='towns'
        )
    sister_towns = models.ManyToManyField('self', blank=True)

    autocomplete = AutocompleteMeta(
        name='town',
        path='%s/town' % API_FILTER_PATH
        )

    class Meta:
        verbose_name = 'Town'


class OrganisationTown(HasDoc, Timestamped):
    """
    The OrganisationTown model. It is the `through` model for Towns and
    Organisations.

        >>> usa = Country.objects.create(name='usa')
        >>> town = Town.objects.create(name='redmond', country=usa)
        >>> org = Organisation.objects.create(name='microsoft')

    Join them with the through table:

        >>> import datetime
        >>> join = OrganisationTown.objects.create(
        ...     joined=datetime.date(2014, 7, 10), town=town,
        ...     organisation=org)

    Clean up

        >>> usa.delete()
        >>> town.delete()
        >>> org.delete()
        >>> join.delete()

    """
    organisation = models.ForeignKey(Organisation)
    town = models.ForeignKey(Town)
    joined = models.DateField()

    autocomplete = AutocompleteMeta(
        name='organisationtown',
        path='%s/organisationtown' % API_FILTER_PATH
        )

    class Meta:
        verbose_name = 'Organisation Town Join'


class TaggedItem(Timestamped, models.Model):
    """
    Simple generic content type example from `django generic relations
    <https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#generic-relations>`_

        >>> town = Town.objects.create(name='Twin Peaks')
        >>> tag = TaggedItem(content_object=town, tag='lynch')
        >>> tag.save()
        >>> tag.content_object
        <Town: Twin Peaks>

    Clean up::

        >>> tag.delete()
        >>> town.delete()

    """
    tag = models.SlugField()
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=models.Q(model__in=['town', 'country', 'organisation']))
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class TestMe(models.Model):
    test_ip = models.IPAddressField(help_text="Lorem dolor")
    test_url = models.URLField(help_text="Lorem dolor")
    test_int = models.IntegerField(help_text="Lorem dolor")
    test_img = models.ImageField(upload_to='dummy', blank=True)
    test_file = models.FileField(upload_to='dummy', blank=True)
    test_date = models.DateField(help_text="Lorem dolor")
    test_char = models.CharField(max_length=50, help_text="Lorem dolor")
    test_bool = models.BooleanField(default=False, help_text="Lorem dolor")
    test_time = models.TimeField(help_text="Lorem dolor")
    test_slug = models.SlugField(help_text="Lorem dolor")
    test_text = models.TextField(help_text="Lorem dolor")
    test_email = models.EmailField(help_text="Lorem dolor")
    test_float = models.FloatField(help_text="Lorem dolor")
    test_bigint = models.BigIntegerField(help_text="Lorem dolor")
    test_positive_integer = models.PositiveIntegerField(help_text="Lorem dolor")
    test_decimal = models.DecimalField(max_digits=5, decimal_places=2, help_text="Lorem dolor")
    test_comma_separated_int = models.CommaSeparatedIntegerField(max_length=100, help_text="Lorem dolor")
    test_small_int = models.SmallIntegerField(help_text="Lorem dolor")
    test_nullbool = models.NullBooleanField(help_text="Lorem dolor")
    test_filepath = models.FilePathField(blank=True, help_text="Lorem dolor")
    test_positive_small_int = models.PositiveSmallIntegerField(help_text="Lorem dolor")

    class Meta:
        verbose_name = u'Test me'
        verbose_name_plural = u'Lot of Test me'


class TestSortable(models.Model):
    that = models.ForeignKey(TestMe)
    position = models.PositiveSmallIntegerField("Position")
    test_char = models.CharField(max_length=5)

    class Meta:
        ordering = ('position', )
