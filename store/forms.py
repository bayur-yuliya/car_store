from django import forms

from .models import Car

class CarForm(forms.ModelForm):
    model = Car
    fields = ['car_type', 'color', 'year']