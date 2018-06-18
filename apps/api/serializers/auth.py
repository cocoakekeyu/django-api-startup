# -*- coding: utf-8 -*-
from rest_framework import serializers

from utils import is_phonenumber


__all__ = ['LoginPermitSerializer', 'ChangePasswordPermitSerializer']


class LoginPermitSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if is_phonenumber(data['account']):
            data['phone'] = data['account']
        else:
            data['username'] = data['account']
        del data['account']
        return data


class ChangePasswordPermitSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
