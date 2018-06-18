# -*- coding: utf-8 -*-
import unittest

import pytest
from model_mommy import mommy

from apps.backend import const
from apps.backend.models import User
from tests.fixtures.client import APIClient


pytestmark = pytest.mark.django_db


class TestAuthLogin(unittest.TestCase):

    def test_login_with_username(self):
        c = APIClient()
        User.objects.create_user(
            username='username', phone='15566667777', password='123456')
        data = {
            'account': 'username',
            'password': '123456',
        }
        response = c.post('/api/v1/auth/login', data)
        r = response.json()
        assert response.status_code == 200
        assert 'access_token' in r

    def test_login_with_phone(self):
        c = APIClient()
        User.objects.create_user(
            username='helloworld', phone='15566667777', password='123456')
        data = {
            'account': '15566667777',
            'password': '123456',
        }
        response = c.post('/api/v1/auth/login', data)
        r = response.json()
        assert response.status_code == 200
        assert 'access_token' in r

    def test_login_failure(self):
        c = APIClient()
        mommy.make_recipe(
            'tests.fixtures.user', username='helloworld',
            phone='15566667777', password='123456')
        data = {
            'account': '15233334444',
            'password': '123456',
        }
        response = c.post('/api/v1/auth/login', data)
        assert response.status_code == 400

    def test_login_failure_with_user_at_admin(self):
        c = APIClient()
        User.objects.create_user(
            username='helloworld', phone='15566667777', password='123456')
        data = {
            'account': '15566667777',
            'password': '123456',
        }
        c._add_client_header(const.ClientAppType.ADMIN.value + '/1.0.0')
        response = c.post('/api/v1/auth/login', data)
        assert response.status_code == 400
