from django import forms
from .models import Profile, AbsUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from .models import Profile



class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')


#
# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = AbsUser
#         fields = ('first_name', 'last_name', "username", 'email','phone_number')
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if AbsUser.objects.filter(email=email).exists():
#             raise forms.ValidationError(' user with this email is already registered -- Try loginigin or resting the password')
#         return email
