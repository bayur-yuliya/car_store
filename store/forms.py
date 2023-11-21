from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username", required=True)
    email = forms.EmailField(label="Email address", required=True)
    password1 = forms.CharField(label="Password", required=True)
    password2 = forms.CharField(label="Password confirmation", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
