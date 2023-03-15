from django import forms

import django_filters
from django_filters.widgets import RangeWidget
from django.forms.widgets import TextInput

from .models import Pet

class PetFilter(django_filters.FilterSet):
    breed = django_filters.CharFilter(lookup_expr = 'icontains', 
                                        label = 'Raza', 
                                        widget = TextInput(attrs = {
                                            'class': 'form-control',
                                            'placeholder': 'raza'
                                            })
                                        )
    sex = django_filters.ChoiceFilter(choices = Pet.SEX_CHOICES,
                                        label = 'Sexo',  
                                        widget = forms.Select(attrs = {
                                            'class': 'form-control'
                                            })
                                        )
    size = django_filters.ChoiceFilter(choices = Pet.SIZE_CHOICES,
                                        label = 'Tamaño',
                                        widget = forms.Select(attrs = {
                                            'class': 'form-control'
                                            })
                                        )
    type_of_pet = django_filters.ChoiceFilter(choices = Pet.TYPE_OF_PET_CHOICES,
                                                label = 'Tipo', 
                                                widget = forms.Select(attrs = {
                                                    'class': 'form-control'
                                                    })
                                                )
    age__gte = django_filters.NumberFilter(field_name='age', 
                                            label = 'edad mayor o igual que', 
                                            lookup_expr='gte',
                                            widget = forms.NumberInput(attrs = {
                                                    'class': 'form-control',
                                                    'min': '0',
                                                    'max': '99'
                                                })
                                            )
    age__lte = django_filters.NumberFilter(field_name='age', 
                                            label = 'edad menor o igual que', 
                                            lookup_expr='lte',
                                            widget = forms.NumberInput(attrs = {
                                                    'class': 'form-control',
                                                    'min': '0',
                                                    'max': '99'
                                                })
                                            )

    class Meta:
        model = Pet
        fields = ['breed', 'sex', 'size', 'type_of_pet']