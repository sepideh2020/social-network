from django.urls import path
from .views import (my_profile_view,
                    invited_received_view,
                    profiles_list_view,
                    invite_profiles_list_view,
                    ProfileListView
                    )


app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('my-invites/', invited_received_view, name='my-invites-view'),
    path('all-profiles/',ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
]
