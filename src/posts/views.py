from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile


# Create your views here.

def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    context = {
        'qs': qs,
        'profile': profile,
    }
    return render(request, 'posts/main.html', context)


def like_unlike_post(request):
    user = request.user  # user that is logged in
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        # check if profile of the user is in many to many field(like field in Post)

        if profile in post_obj.liked.all():
            # because the profile is already in the liked.all(),if the profile
            # liked the post again we should remove  the profile
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        # user is the foreign key to profile
        # if created is equal to True this means  that the post didnt exist before it created
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

    return redirect('posts:main-post-view')
