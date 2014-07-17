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
        required=False,
        )
    documentation = forms.ModelMultipleChoiceField(
        queryset=Documentation.objects.all(),
        widget=AutocompleteSelectMultipleWidget,
        required=False,
        )

    class Meta:
        model = Country
        fields = ['name', 'towns', 'documentation']

    # Overriding __init__ here allows us to provide initial
    # data for 'towns' field
    def __init__(self, *args, **kwargs):

        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})

            if kwargs['instance']:
                initial['towns'] = [t.pk for t in kwargs['instance'].town_set.all()]
                initial['documentation'] = [t.pk for t in kwargs['instance'].documentation.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

        rel = ManyToManyRel(self._meta.model.documentation.field.rel.to, Country, 'documentation')

        # wrapping the widgets gives the field the `add` button
        self.fields['documentation'].widget = RelatedFieldWidgetWrapper(
            self.fields['documentation'].widget, rel, self.admin_site)

        rel = ManyToOneRel(self._meta.model.town_set.related, Town, 'country')

        self.fields['towns'].widget = RelatedFieldWidgetWrapper(
            self.fields['towns'].widget, rel, self.admin_site)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        instance.save()
        instance.town_set = self.cleaned_data['towns']
        instance.documentation = self.cleaned_data['documentation']
        self.save_m2m()
        return instance
