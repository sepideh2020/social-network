from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # every user will have his own profile/every time the user is deleted the profile is deleted as well
    bio = models.TextField(default='no bio ...', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')  # profile picture
    # install pillow
    # create media_root
    # find avatar.png
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    # slug is base on first name and last name if they are provided otherwise slug is made out of the user
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        # instead of author_set.all() we wrote posts.all() because author verbose_name is posts
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        """this function counts all likes of a particular post"""
        posts = self.posts.all()  # gets all posts of a particular profile
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.created.strftime(('%d-%m-%Y')))

    def save(self, *args, **kwargs):
        """this function is for making slug for users , Ones whose first and last name are similar
        and for ones who do not have first name and last name ,if a user does not have first and last name,
        his slug is made based on user. for making unique slug we used  get_random_code() function which is
        defined at utils.py"""
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    # who sends invitation
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    # who receives the invitation
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    # whether it is sent,accepted,ignored or deleted
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.sender, self.receiver, self.status)
