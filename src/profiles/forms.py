from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class SignUpForm(UserCreationForm):
    """
    form for Signup
    """

    class Meta:
        model = CustomUser
        fields = (
            'username', 'phone', 'email', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None and cleaned_data.get('phone') is None:
            raise ValidationError('Please Enter an Email or a Phone number')
        return cleaned_data


class LoginForm(AuthenticationForm):
    """
    Form for logging
    """
    username = forms.CharField(label='Email / Username/phone')


class ProfileModelForm(forms.ModelForm):
    """
    Form for updating user profile
    """

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio','gender', 'website', 'avatar')
