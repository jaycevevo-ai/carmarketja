from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'title',
            'make',
            'model',
            'year',
            'price',
            'mileage',
            'transmission',
            'fuel_type',
            'color',
            'location',
            'description',
            'image',
        ]