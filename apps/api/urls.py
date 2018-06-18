# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework import routers

from apps.api.views.user import UserViewSet
from apps.api.views.auth import (
    LoginView, ChangePasswordView
)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='user')


urlpatterns = [
    url(r'^auth/login/?$', LoginView.as_view()),
    url(r'^auth/change_pass/?$', ChangePasswordView.as_view()),
]


urlpatterns += router.urls
