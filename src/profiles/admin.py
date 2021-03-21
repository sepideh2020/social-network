from django.contrib import admin
from .models import Profile, Relationship, User

# Register your models here.
admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(User)
