from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
