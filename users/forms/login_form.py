from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
