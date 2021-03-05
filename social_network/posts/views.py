from django.shortcuts import render, redirect
from posts.forms import CommentModelForm, PostModelForm
from posts.models import Post, Like
from profiles.models import Profile


def post_comment_create_and_list_view(request):
    """
    This function is for add a post by user and add a comment below of post
    :param request: sometimes request.user
    :return: add data to DB
    """
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    # initial value of PostForm and CommentForm and PostAdded because if load form and dont add any thing in form we get
    # error
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)
    # submit_p_form is name of submit button in main.html
    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            # we use commit=False when I want add a instance to DB but we want add a value to feature other time
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)


def like_unlike_post(request):
    """
    This function manage like and dislike a post
    :param request: sometimes request.user
    :return: add like instance to DB like table
    """
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

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
