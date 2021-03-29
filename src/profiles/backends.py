from django.contrib.auth.backends import ModelBackend

from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from profiles.models import CustomUser
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class PhoneEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username) | Q(phone__iexact=username))
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
        except MultipleObjectsReturned:
            return CustomUser.objects.filter(email=username).order_by('id').first()
        # except:
        #     return CustomUser.objects.filter(phone=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


