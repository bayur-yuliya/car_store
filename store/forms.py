from django import forms

from store.models import Car


class CarPhotoChange(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('photo',)
