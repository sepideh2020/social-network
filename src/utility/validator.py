from django.core.exceptions import ValidationError
from .constant import WEBSITE_REGEX, PHONE_REGEX, USERNAME_REGEX
import re



def confirm_website(website):
    """
        check value of website field in customuser model with pattern for sure it`s correct or not
    """
    pattern = WEBSITE_REGEX
    if not re.search(pattern, website):
        raise ValidationError('your website is invalid')


def confirm_phone(phone):
    """
    check value of phone field in costomuser model with pattern for sure it`s correct or not
    """
    pattern = PHONE_REGEX
    if not re.search(pattern, phone):
        raise ValidationError('your phone number is invalid')


def confirm_username(user_name):
    """
        check value of user_name field in customuser model with pattern for sure it`s correct or not
    """
    pattern = USERNAME_REGEX
    if not re.search(pattern, user_name):
        raise ValidationError('invalid user name')



