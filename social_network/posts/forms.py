from django import forms
from .models import Comment, Post


class CommentModelForm(forms.ModelForm):
    """
    This form added for send a comment below a post
    """
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)


class PostModelForm(forms.ModelForm):
    """
    This form added for send a post
    """
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Post
        fields = ('content', 'image')
