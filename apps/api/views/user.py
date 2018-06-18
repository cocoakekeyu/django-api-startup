# -*- coding: utf-8 -*-
import logging

from rest_framework.response import Response

from .base import BaseViewSet
from apps.backend.models import User
from apps.api.serializers import (
    UserSerializer, UserDetailSerializer, UserPermitSerializer
)
from apps.api.auth import authorize
from utils import sub_dict


logger = logging.getLogger('mylogger')


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    search_fields = ('name', 'username')
    serializer_class = UserSerializer

    @authorize('read', User)
    def list(self, request):
        return self.get_list_response()

    def retrieve(self, request, pk):
        user = self.get_object()
        authorize(request.user, 'read', user)
        serializer = self.get_serializer(
            user, serializer_class=UserDetailSerializer)
        return Response(serializer.data)

    @authorize('create', User)
    def create(self, request):
        serializer = UserPermitSerializer(data=request.data)
        serializer.is_valid(True)

        # Create user with object.create_user
        user = User.objects.create_user(**serializer.validated_data)
        serializer = self.get_serializer(
            user, serializer_class=UserSerializer)
        return Response(serializer.data, status=201)

    def update(self, request, pk):
        user = self.get_object()
        authorize(request.user, 'update', user)
        data = dict(request.data)

        # User can only update 'name'
        if not self.is_superuser:
            data = sub_dict(data, ['name'])

        serializer = UserPermitSerializer(
            user, data=data, partial=True)
        serializer.is_valid(True)
        user = serializer.save()
        serializer = self.get_serializer(
            user, serializer_class=UserDetailSerializer)
        return Response(serializer.data)

    def destroy(self, request, pk):
        user = self.get_object()
        authorize(request.user, 'destroy', user)
        logger.info('{} deleted user: {}'
                    .format(self.current_user, user))
        user.delete()
        return Response(status=204)
