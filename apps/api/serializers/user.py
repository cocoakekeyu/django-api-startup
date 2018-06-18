# -*- coding: utf-8 -*-
from rest_framework import serializers

from apps.backend.models import User
from .base import BaseModelSerializer


__all__ = ['UserSimpleSerializer', 'UserSerializer',  'UserDetailSerializer',
           'UserPermitSerializer']


class UserSimpleSerializer(BaseModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name')


class UserSerializer(UserSimpleSerializer):

    class Meta:
        model = User
        fields = UserSimpleSerializer.Meta.fields + \
            ('username', 'phone', 'role')


class UserDetailSerializer(UserSerializer):

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + \
            ('date_joined', 'created_at', 'updated_at')


class UserPermitSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'phone', 'name', 'role', 'password')

    def update(self, user, data):
        if data.get('password'):
            user.set_password(data['password'])
            del data['password']
        return super().update(user, data)
