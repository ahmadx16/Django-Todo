from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget())
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'bio',
        ]

    def save(self, request, commit=True):
        request.user.first_name = self.cleaned_data['first_name']
        request.user.last_name = self.cleaned_data['last_name']
        request.user.email = self.cleaned_data['email']
        request.user.profile.bio = self.cleaned_data['bio']
        request.user.profile.date_of_birth = self.cleaned_data['date_of_birth']
        request.user.save()
        return request.user
