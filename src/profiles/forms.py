from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .validators import mobile_validator, mobile_len_validator


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'phone', 'email', 'password1', 'password2',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None and cleaned_data.get('phone') is None:
            raise ValidationError('Please Enter an Email or a Phone number')

        # if cleaned_data.get('phone')[0:4] != '+989':
        #     raise ValidationError('Invalid mobile,length of mobile should be 13 and start with +989')
        #
        # if len(cleaned_data.get('phone')) != 13:
        #     raise ValidationError('Invalid mobile,length of mobile should be 13 and start with +989')
        #
        # username = cleaned_data.get('username')
        # user = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
        # if username == user:
        #     raise ValidationError('Username "%s" is already in use.' % username)

        return cleaned_data






class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username','phone', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username/phone')



class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'website', 'avatar')
