from django import forms

from .models import Car, CarType, Client


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


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone"]
