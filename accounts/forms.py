from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(required=True)
    branch = forms.CharField(max_length=50)
    # customize username to be the roll_no

    class Meta:
        model = User
        fields = ["username", "name", "email",
                  "branch", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(label="Roll no", required=True)
    password = forms.CharField(required=True)
