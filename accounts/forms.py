from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    email = forms.EmailField(max_length=255, required=True, label="Email")

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "phone_number", "email", "password1", "password2"]
