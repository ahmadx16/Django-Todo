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

    def save(self, commit=True):
        self.instance.profile.date_of_birth = self.cleaned_data.get('date_of_birth',)
        self.instance.profile.bio = self.cleaned_data.get('bio',)

        super(ProfileForm, self).save()
        return self.instance
