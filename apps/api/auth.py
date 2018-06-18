# -*- coding: utf-8 -*-
import functools

import cancan
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework_jwt.settings import api_settings

from apps.api.serializers import UserSimpleSerializer
from apps.backend.models import User
from apps.backend import const


class Ability(cancan.Ability):
    def __init__(self, user):
        self.user = user

        if user is None or not user.is_authenticated:
            self.init_guest_ability()
        elif user.is_superuser:
            self.init_superuser_ability()
        elif user.is_admin:
            self.init_admin_ability()
        elif user.role == const.UserRole.USER.value:
            self.init_user_ability()

    def init_guest_ability(self):
        pass

    def init_user_ability(self):
        self.add('change', 'password')

    def init_admin_ability(self):
        self.init_superuser_ability()

    def init_superuser_ability(self):
        self.add('manage', 'all')
        self.addnot('destroy', User, id=self.user.id)


class authorize(object):

    def __init__(self, *args):
        assert 1 < len(args) <= 3
        if len(args) == 2:
            self.user = None
            self.action = args[0]
            self.subject = args[1]
        else:
            user = args[0]
            action = args[1]
            subject = args[2]
            if Ability(user).cannot(action, subject):
                raise PermissionDenied

    def __call__(self, func):
        action = self.action
        subject = self.subject

        @functools.wraps(func)
        def wrapped(instance, request, *args, **kwargs):
            user = request.user
            if Ability(user).cannot(action, subject):
                raise PermissionDenied
            return func(instance, request, *args, **kwargs)

        return wrapped


# jwt utils
def jwt_generate_token(user):
    """Generate jwt token for user.

    return:
        {
            "access_token": "the token",
            "expired_at": "exipred_at time"
        }
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    expired_at = (timezone.now() + api_settings.JWT_EXPIRATION_DELTA)
    result = {
        'access_token': token,
        'expired_at': expired_at
    }
    return result


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'access_token': token,
        'user': UserSimpleSerializer(user, context={'request': request}).data
    }


class PhoneBackend(object):

    def authenticate(self, request, phone, password):
        user = User.objects.filter(phone=phone).first()
        if user and user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
