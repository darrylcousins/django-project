# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

from django_autocomplete.widgets import SmallTextareaWidget
from django_autocomplete.widgets import AutocompleteSelectWidget
from django_autocomplete.widgets import AutocompleteSelectMultipleWidget
from django_autocomplete.forms import searchform_factory

from .models import Town
from .models import Country
from .models import Organisation
from .models import OrganisationTown
from .models import Documentation
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


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']
    search_fields = ['name']
    list_editable = ['name']
    list_per_page = 10
    save_as = True
    date_hierarchy = 'created'
    fields = ['name', 'documentation']
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES


class DocumentationAdmin(BaseAdmin):
    model = Documentation
    search_form = searchform_factory(Documentation)
    fields = ['name']


class TownAdmin(BaseAdmin):
    model = Town
    search_form = searchform_factory(Town)
    inlines = [
        OrganisationTownInline,
        ]


class CountryAdmin(BaseAdmin):
    # this one has the form defined to give direct ediing of m2m town_set
    form = CountryForm
    search_form = searchform_factory(Country)
    fields = ['name', 'towns', 'documentation']

    def __init__(self, model, admin_site):
        super(CountryAdmin, self).__init__(model, admin_site)
        self.form.admin_site = admin_site  # capture the admin_site for the form


class OrganisationAdmin(BaseAdmin):
    model = Organisation
    search_form = searchform_factory(Organisation)
    inlines = [
        TownOrganisationInline,
        ]


class OrganisationTownAdmin(admin.ModelAdmin):
    model = OrganisationTown
    fields = ['organisation', 'town', 'joined', 'documentation']
    list_display = ['custom_name', 'created', 'modified']
    save_as = True
    date_hierarchy = 'created'
    search_form = searchform_factory(OrganisationTown)
    formfield_overrides = DEFAULT_FORMFIELD_OVERRIDES

    def custom_name(self, obj):
        return ("%s - %s" % (obj.town.name, obj.organisation.name))
    custom_name.short_description = 'Name'

# Register your models here.
admin.site.register(Town, TownAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Documentation, DocumentationAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(OrganisationTown, OrganisationTownAdmin)
