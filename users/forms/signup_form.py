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

    def clean(self):
        super(SignupForm, self).clean()

        # Validates whether both passwords matches
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password == password2:
            raise forms.ValidationError('Passwords must match')

    def save(self, commit=True):

        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
