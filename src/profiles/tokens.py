import datetime
from random import randint

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone
from kavenegar import KavenegarAPI, HTTPException, APIException

from posts import models
from social_network.settings import Kavenegar_API
from .models import CustomUser
from datetime import datetime, timezone


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(CustomUser.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()


def send_otp(phone, otp):
    phone = [phone, ]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '1000596446',  # optional
            'receptor': phone,  # multiple mobile number, split by comma
            'message': 'Your OTP is {}'.format(otp),
        }
        response = api.sms_send(params)
        print('OTP: ', otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(1000, 9999)


def check_otp_expiration(phone):
    try:
        user = models.CustomUser.objects.get(phone=phone)
        now = datetime.now(timezone.utc)
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)

        if diff_time.seconds > 120:
            return False
        return True

    except models.CustomUser.DoesNotExist:
        return False
