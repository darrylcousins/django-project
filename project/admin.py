# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from django_admin_bootstrapped.admin.models import SortableInline

from django_autocomplete.widgets import SmallTextareaWidget
from django_autocomplete.widgets import AutocompleteSelectWidget
from django_autocomplete.widgets import AutocompleteSelectMultipleWidget
from django_autocomplete.widgets import AutocompleteCTWidget
from django_autocomplete.forms import searchform_factory

from .models import Town
from .models import Country
from .models import Organisation
from .models import OrganisationTown
from .models import Documentation
from .models import TaggedItem
from .models import TestMe
from .models import TestSortable
from .forms import CountryForm


DEFAULT_FORMFIELD_OVERRIDES = {
    models.TextField: {'widget': SmallTextareaWidget},
    models.ForeignKey: {'widget': AutocompleteSelectWidget},
    models.ManyToManyField: {'widget': AutocompleteSelectMultipleWidget},
    }


class BaseInline(admin.TabularInline):
    extra = 0
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES
    fields = ['name', 'documentation']


class OrganisationTownInline(BaseInline):
    model = OrganisationTown
    verbose_name = 'Organisation'
    verbose_name_plural = '%ss' % verbose_name
    fields = ['organisation', 'joined', 'documentation']


class TownOrganisationInline(BaseInline):
    model = OrganisationTown
    verbose_name = 'Town'
    verbose_name_plural = '%ss' % verbose_name
    fields = ['town', 'joined', 'documentation']


class CountryInline(BaseInline):
    model = Country


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    verbose_name = 'Tag'
    verbose_name_plural = '%ss' % verbose_name


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']
    search_fields = ['name']
    list_editable = ['name']
    list_filter = ['created', 'modified']
    list_per_page = 10
    save_as = True
    date_hierarchy = 'created'
    fields = ['name', 'documentation']
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        super(BaseAdmin, self).save_formset(request, form, formset, change)
        formset.save_m2m()

        return form.save(commit=False)


@admin.register(Documentation)
class DocumentationAdmin(BaseAdmin):
    model = Documentation
    search_form = searchform_factory(Documentation)
    search_fields = ['name']
    fields = ['name']


@admin.register(Town)
class TownAdmin(BaseAdmin):
    model = Town
    search_form = searchform_factory(Town)
    search_fields = ['name']
    fields = ['name', 'sister_towns', 'documentation']
    inlines = [
        OrganisationTownInline,
        TaggedItemInline
        ]


class CountryAdmin(BaseAdmin):
    # this one has the form defined to give direct ediing of m2m town_set
    form = CountryForm
    search_form = searchform_factory(Country)
    fields = ['name', 'towns', 'documentation']
    inlines = [
        TaggedItemInline
        ]

    def __init__(self, model, admin_site):
        super(CountryAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site  # capture the admin_site for the form

admin.site.register(Country, CountryAdmin)


@admin.register(Organisation)
class OrganisationAdmin(BaseAdmin):
    model = Organisation
    search_form = searchform_factory(Organisation)
    search_fields = ['name']
    inlines = [
        TownOrganisationInline,
        TaggedItemInline
        ]


@admin.register(OrganisationTown)
class OrganisationTownAdmin(admin.ModelAdmin):
    model = OrganisationTown
    fields = ['organisation', 'town', 'joined', 'documentation']
    list_display = ['custom_name', 'created', 'modified']
    search_fields = ['town__name', 'organisation__name']
    save_as = True
    date_hierarchy = 'created'
    search_form = searchform_factory(OrganisationTown)
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES

    def custom_name(self, obj):
        return ("%s - %s" % (obj.town.name, obj.organisation.name))
    custom_name.short_description = 'Name'


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    model = TaggedItem
    search_fields = ['tag']
    formfield_overrides = {
        models.ForeignKey: {'widget': AutocompleteCTWidget},
        }


class TestSortable(admin.TabularInline, SortableInline):
    model = TestSortable
    start_collapsed = True
    extra = 0


@admin.register(TestMe)
class TestMeAdmin(admin.ModelAdmin):
    search_fields = ['test_ip', 'test_url', ]
    list_editable = ['test_int', ]
    list_filter = ['test_ip', 'test_url', 'test_int', ]
    list_per_page = 3
    date_hierarchy = 'test_date'
    inlines = [TestSortable]
    save_as = True
    save_on_top = True
    list_display = [
        'test_ip',
        'test_url',
        'test_int',
        'test_date',
        'test_char',
        'test_bool',
        'test_time',
        'test_slug',
        'test_email',
        'test_float',
        'test_bigint',
        'test_positive_integer',
        'test_decimal',
        'test_comma_separated_int',
        'test_small_int',
        'test_nullbool',
        'test_positive_small_int'
        ]
    fieldsets = (
        (None, {
            'fields': ('test_ip', 'test_url')
        }),
        ('A fieldset', {
            'classes': ('collapse',),
            'fields': (
                'test_int',
                'test_file',
                'test_date',
                'test_char',
                'test_bool',
                'test_time',
                'test_slug',
                'test_text'
                ),
        }),
        ('Another fieldset', {
            'classes': ('collapse',),
            'fields': (
                'test_email',
                'test_float',
                'test_bigint',
                'test_positive_integer',
                'test_decimal',
                'test_comma_separated_int',
                'test_small_int',
                'test_nullbool',
                'test_filepath',
                'test_positive_small_int'
                ),
        }),
    )
