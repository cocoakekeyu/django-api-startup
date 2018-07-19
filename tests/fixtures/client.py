# -*- coding: utf-8 -*-
import pytest
from rest_framework.test import APIClient as RESTAPIClient
from django.test import Client as DjangoClient

from apps.backend.models import User
from apps.backend import const
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


__all__ = ['APIClient', 'DjangoClient']


class APIClient(RESTAPIClient):

    def __init__(self, *args, **kwargs):
        super(APIClient, self).__init__(*args, **kwargs)

    def login_user(self):
        self._user = User.objects.create_user(username='17721213131',
                                              phone='17721213131',
                                              password='123456')
        self._add_credentials()
        self._add_client_header(const.ClientAppType.WEB.value + '/1.0.0')

    def login_superuser(self):
        self._user = User.objects.create_superuser(username='15521213131',
                                                   phone='15521213131',
                                                   password='123456')
        self._add_credentials()
        self._add_client_header(const.ClientAppType.ADMIN.value + '/1.0.0')

    def _add_credentials(self):
        payload = jwt_payload_handler(self._user)
        token = jwt_encode_handler(payload)
        self.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))

    def _add_client_header(self, client_type):
        if client_type:
            self._client_type = {'HTTP_X_APP': client_type}

    def request(self, **kwargs):
        if getattr(self, '_client_type', None):
            kwargs.update(self._client_type)
        return super(APIClient, self).request(**kwargs)


@pytest.fixture
def client():
    """APIClient"""
    return APIClient()


@pytest.fixture
def client_user():
    """APIClient login with user"""
    c = APIClient()
    c.login_user()
    return APIClient()


@pytest.fixture
def client_superuser():
    """APIClient login with superuser"""
    c = APIClient()
    c.login_superuser()
    return c
