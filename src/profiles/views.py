from django.shortcuts import render
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User


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


def invite_profiles_list_view(request):
    """profiles list available to invite"""
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)


def profiles_list_view(request):
    """get all profiles by method view"""
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)


class ProfileListView(ListView):
    """get all profiles by list view"""
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        """this function allows us to some additional context to the template"""

        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)  # it gets user the user
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        # relationships where we invited other users
        rel_s = Relationship.objects.filter(receiver=profile)
        # relationships where we are receiver of the invitation
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            # if we will be the only profile 'is_empty' will be equall to True
            context['is_empty'] = True
        return context
