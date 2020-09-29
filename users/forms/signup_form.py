from django import forms

from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'password2',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
