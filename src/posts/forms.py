from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    """
        content overridden because we wanted our form have just 2 row,
        this form is for adding posts by which user cant add post image and content post
    """

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    class Meta:
        model = Post
        fields = ('content', 'image',)


class CommentModelForm(forms.ModelForm):
    """
        this form is for adding Comment for posts
    """
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
