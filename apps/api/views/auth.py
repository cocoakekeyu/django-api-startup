# -*- coding: utf-8 -*-
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.api.serializers import (
    UserSerializer, LoginPermitSerializer, ChangePasswordPermitSerializer,
)
from apps.api.exceptions import ViewException
from apps.api.auth import jwt_generate_token, authorize
from apps.backend import const
from .base import BaseAPIView


class LoginView(BaseAPIView):
    authentication_classes = ()

    def post(self, request):
        serializer = LoginPermitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)

        user = authenticate(**serializer.validated_data)
        if not user or not user.is_active:
            msg = err = '用户名或者密码错误'
            raise ViewException(msg, err)

        # Only staff can login in admin backend
        if self.current_app == const.ClientAppType.ADMIN.value:
            if not user.is_staff:
                msg = err = '用户名或者密码错误'
                raise ViewException(msg, err)

        user.last_login = timezone.now()
        user.save()

        response_data = {
            'user': UserSerializer(user).data
        }
        token = jwt_generate_token(user)
        response_data.update(token)
        return Response(response_data)


class ChangePasswordView(APIView):

    @authorize('change', 'password')
    def post(self, request):
        user = request.user
        serializer = ChangePasswordPermitSerializer(data=request.data)
        serializer.is_valid(True)
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
        else:
            msg = err = '密码错误'
            raise ViewException(msg, err)
        return Response()
