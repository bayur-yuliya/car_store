from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from store.models import Car


class RegisterUserForm(SignupForm, UserCreationForm):
    username = forms.CharField(label="Username", required=True)
    email = forms.EmailField(label="Email address", required=True)
    password1 = forms.CharField(label="Password", required=True)
    password2 = forms.CharField(label="Password confirmation", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(RegisterUserForm, self).save(request)
        # Add your own processing here.
        # You must return the original result.
        return user


class CarPhotoChangeForm(forms.ModelForm):
    photo = forms.ImageField(label="Выберите картинку: ", widget=forms.FileInput)

    class Meta:
        model = Car
        fields = ("photo",)
