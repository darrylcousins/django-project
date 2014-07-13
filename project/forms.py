# -*- coding: utf-8 -*-
from django import forms
from django.db.models import ManyToOneRel
from django.db.models import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from django_autocomplete.widgets import AutocompleteSelectMultipleWidget

from .models import Town
from .models import Country
from .models import Documentation


class CountryForm(forms.ModelForm):
    """
    Mostly lifted from
    http://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
    """

    name = forms.CharField()
    # Representing the many to many related field `town_set`
    towns = forms.ModelMultipleChoiceField(
        queryset=Town.objects.all(),
        widget=AutocompleteSelectMultipleWidget,
        )
    documentation = forms.ModelMultipleChoiceField(
        queryset=Documentation.objects.all(),
        widget=AutocompleteSelectMultipleWidget,
        )

    class Meta:
        model = Country
        fields = ['name', 'towns', 'documentation']

    # Overriding __init__ here allows us to provide initial
    # data for 'towns' field
    def __init__(self, *args, **kwargs):

        # Only in case we build the form from an instance
        # (otherwise, 'towns' list should be empty)
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})

            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['towns'] = [t.pk for t in kwargs['instance'].town_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

        rel = ManyToManyRel(self.instance.documentation.model, Country, 'documentation')

        # wrapping the widgets gives the field the `add` button
        self.fields['documentation'].widget = RelatedFieldWidgetWrapper(
            self.fields['documentation'].widget, rel, self.admin_site)

        rel = ManyToOneRel(self.instance.town_set.model, Town, 'country')
        self.fields['towns'].widget = RelatedFieldWidgetWrapper(
            self.fields['towns'].widget, rel, self.admin_site)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        # clear will work if the ForeignKey has null=True and then the set can
        # be replaced in bulk

        # instance.town_set.clear()
        # for town in self.cleaned_data['towns']:
        #    instance.town_set.add(town)
        instance.town_set = self.cleaned_data['towns']
        instance.documentation = self.cleaned_data['documentation']

        if commit:
            instance.save()
            self.save_m2m()
        return instance
