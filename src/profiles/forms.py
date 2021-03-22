from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import mobile_validator, mobile_len_validator


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'user_name', 'phone', 'email', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None and cleaned_data.get('phone') is None:
            raise ValidationError('Please Enter an Email or a Phone number')

        if cleaned_data.get('phone')[0:4] != '+989':
            raise ValidationError('Invalid mobile,length of mobile should be 13 and start with +989')

        if len(cleaned_data.get('phone')) != 13:
            raise ValidationError('Invalid mobile,length of mobile should be 13 and start with +989')

        # username = cleaned_data.get('user_name')
        # user = CustomUser.objects.exclude(pk=self.instance.pk).get(user_name=username)
        # if username == user:
        #     raise ValidationError('Username "%s" is already in use.' % username)

        return cleaned_data


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'website', 'avatar')
