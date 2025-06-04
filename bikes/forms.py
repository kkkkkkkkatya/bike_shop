from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class OrderForm(forms.Form):
    bike_type = forms.ChoiceField(
        choices=[("regular", "Звичайний"), ("electric", "Електричний")]
    )
