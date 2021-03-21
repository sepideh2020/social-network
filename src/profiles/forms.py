from django import forms
from .models import CustomUser


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'website', 'avatar')
