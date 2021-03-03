from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post
from profiles.models import Profile


# def post_comment_create_and_list_view(request):
#     qs = Post.objects.all()
#
#     context = {
#         'qs': qs,
#
#     }
#
#     return render(request, 'posts/main.html', context)


class PostCommentCreateAndListView(ListView):
    """
    This class show ListPost of user log in
    """
    model = Post
    template_name = 'posts/main.html'
