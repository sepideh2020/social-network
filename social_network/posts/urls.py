from django.urls import path

from .views import PostCommentCreateAndListView

app_name = 'posts'
urlpatterns = [
    path('', PostCommentCreateAndListView.as_view(), name='main-post-view'),

]
