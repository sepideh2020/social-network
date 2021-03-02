from django.contrib import admin

# Register your models here.
from profiles.models import Profile, Relationship


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created']


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
