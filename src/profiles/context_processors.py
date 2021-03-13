from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        # context processors are always returning dictionary
        return {'picture': pic}
    return {}


def invitation_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitation_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}

