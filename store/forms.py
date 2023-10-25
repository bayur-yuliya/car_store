from django import forms

from .models import Car, Client


class CarForm(forms.ModelForm):
    color = forms.ModelChoiceField(label="",
        queryset=Car.objects.all(),
    )
    amount = forms.DecimalField()

    class Meta:
        model = Car
        fields = ["car_type", "color"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone"]
