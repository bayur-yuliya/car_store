from django import forms

from .models import Car, CarType


class CarForm(forms.ModelForm):
    car_type = forms.ModelChoiceField(queryset=CarType.objects.all())

    color = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    amount = forms.DecimalField()

    class Meta:
        model = Car
        fields = ["car_type", "color"]
