from profiles.models import CustomUser, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        print(request.user.id)
        profile_obj = CustomUser.objects.get(id__exact=request.user.id)
        pic = profile_obj.avatar
        return {'picture': pic}
    return {}


def invatations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = CustomUser.objects.get(id__exact=request.user.id)
        qs_count = Relationship.objects.invitation_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}
