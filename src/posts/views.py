from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm


# Create your views here.

def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    # before saving form we need to have author to be assigned to the field of author in the post model so
    # we need to get the profile be request.user

    # initial
    p_form = PostModelForm()
    # we used request.Files because we might send an image
    c_form = CommentModelForm()
    post_added = False
    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        # print(request.POST)
        p_form = PostModelForm(request.POST, request.FILES)

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()  # our form loads again for writing a new post
            post_added = True
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            # gets the id of the post which the user us commenting on
            instance.save()
            c_form = CommentModelForm()  # resets the form

    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,

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
