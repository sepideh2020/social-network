from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from social_network import settings



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, user_name, password, **extra_fields):
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(user_name, password, **extra_fields)

    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(user_name, password, **extra_fields)

    def get_all_profiles_to_invite(self, sender):
        """gets all the profiles that are available for us to invite so cases of profiles where we are already
        in a relationship with were excluded.
        Here the sender is ourselves and the receiver is different user with whom we dont have a relationship status
        set to 'accepted' """

        profiles = CustomUser.objects.all().exclude(id__exact=sender.id)
        profile = CustomUser.objects.get(id__exact=sender.id)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        # grabbed all the relationships where we are the sender or receiver

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                # because are either receiver or sender using set prevents repetition in list
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if
                     profile not in accepted]  # all the available profile to invite
        print(available)
        return available

    def get_all_profiles(self, me):
        """gets all the profiles that are in the system excluding our own"""

        profiles = CustomUser.objects.all().exclude(id__exact=me.id)
        return profiles


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    this class create a new user
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(_('Username'), max_length=100, unique=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')  # profile picture
    phone_number = models.CharField(_('Phone number'), max_length=11, blank=True, null=True, unique=True)
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, null=True)
    bio = models.TextField(default='no bio ...', max_length=300)
    country = models.CharField(max_length=200, blank=True)
    website = models.CharField(_('Website'), blank=True, max_length=150)
    email = models.EmailField("email address", blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    objects = CustomUserManager()

    def __str__(self):
        return '{}-{}'.format(self.username, self.created.strftime('%d-%m-%Y'))

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_username = self.username

    def save(self, *args, **kwargs):
        """this function is for making slug for users , Ones whose first and last name are similar
        and for ones who do not have first name and last name ,if a user does not have first and last name,
        his slug is made based on user. for making unique slug we used  get_random_code() function which is
        defined at utils.py"""
        self.slug = slugify(str(self.username))
        super().save(*args, **kwargs)
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):

    def invitation_received(self, receiver):
        """shows all the invitation we received from different users and the receiver is going to be our selves"""
        # we passed the profile as the receiver because the receiver is foreign key to  our profile
        # instead of writing  a view like Relationship.objects.invitation_receiver(my_profile) we wrote a model#??
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        # status chosen from STATUS_CHOICES
        # if the receiver accepts the invitation it no longer exists
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    # who sends invitation
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    # who receives the invitation
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    # whether it is sent,accepted,ignored or deleted
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager()

    def __str__(self):
        return '{}-{}-{}'.format(self.sender, self.receiver, self.status)
