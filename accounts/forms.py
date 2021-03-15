from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            q = User.objects.filter(email=email)
            if q.exists():
                raise forms.ValidationError('이미 등록된 이메일 주소입니다.')
        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar': 'Profile Image',
        }
