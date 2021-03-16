from django.core.validators import FileExtensionValidator
from django.db import models

from profiles.models import Profile


class Post(models.Model):
    """
    This class present Post model that refers one Post
    """
    content = models.TextField()
    # FileExtensionValidator Raises a ValidationError with a
    # code of 'invalid_extension' if the extension of value.name
    # (value is a File) isn’t found in allowed_extensions.
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                              blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        """
         :return:likes.no of a post
        """
        return self.liked.all().count()

    def num_comments(self):
        """
        :return:comments.no of a post
        """
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)  # newest post is top


class Comment(models.Model):
    """
    This class present Comment model that refers one comment
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    """
    This class present Like model that refers one Like
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
