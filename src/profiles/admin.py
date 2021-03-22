from django.contrib import admin
from .models import CustomUser, Relationship


# Register your models here.

@admin.register(CustomUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name']


@admin.register(Relationship)
class PostAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status']
