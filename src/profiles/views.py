from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    # instance shows us which profile we want to update
    confirm = False

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)


def invited_received_view(request):
    """gets all the invitations for a particular profile"""
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_received(profile)
    context = {'qs': qs}
    return render(request, 'profiles/my_invites.html', context)


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)


def invite_profiles_list_view(request):
    """profiles list available to invite"""
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)
