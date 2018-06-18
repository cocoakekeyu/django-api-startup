# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView

from apps.backend import const


class CommonMixin:

    def get_serializer(self, *args, **kwargs):
        serializer_class = kwargs.pop('serializer_class', None)
        if serializer_class:
            kwargs['context'] = self.get_serializer_context()
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_list_response(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'current_app': self.current_app,
            'current_user': self.current_user,
            'is_staff': self.is_staff,
            'is_admin': self.is_admin,
            'is_superuser': self.is_superuser,
        })
        return context

    @property
    def current_user(self):
        user = self.request.user
        return user if user.is_authenticated else None

    @property
    def current_app(self):
        request = self.request
        app = request.META.get('HTTP_X-APP') or request.META.get('HTTP_X_APP')
        if app:
            app = app.split('/', 1)[0]
            if app in const.ClientAppType.values:
                return app
        return None

    @property
    def is_staff(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff and \
                self.current_app == const.ClientAppType.ADMIN.value:
            return True
        return False

    @property
    def is_admin(self):
        user = self.request.user
        if user.is_authenticated and user.is_admin and \
                self.current_app == const.ClientAppType.ADMIN.value:
            return True
        return False

    @property
    def is_superuser(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser and \
                self.current_app == const.ClientAppType.ADMIN.value:
            return True
        return False


class BaseViewSet(CommonMixin, viewsets.GenericViewSet):
    lookup_value_regex = '\d+'


class BaseAPIView(CommonMixin, GenericAPIView):
    pass
