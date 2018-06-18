# -*- coding: utf-8 -*-
import random
import unittest

import pytest
from model_mommy import mommy

from apps.backend.models import User
from apps.backend import const
from tests.fixtures.client import APIClient
from tests.fixtures import helper


pytestmark = pytest.mark.django_db


class TestUser(unittest.TestCase):
    user_fields = {'name', 'phone', 'role', 'username'}
    user_detail_fields = user_fields | \
        {'date_joined', 'created_at', 'updated_at'}

    def setUp(self):
        self.users = mommy.make_recipe('tests.fixtures.user', _quantity=20)
        self.user = random.choice(self.users)

    def test_list_users(self):
        c = APIClient()
        c.login_superuser()
        response = c.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        r = response.json()
        for item in r:
            assert self.user_fields.issubset(set(item.keys()))

    def test_search_users(self):
        c = APIClient()
        c.login_superuser()
        user = self.user
        response = c.get('/api/v1/users?q={}'.format(user.name))
        self.assertEqual(response.status_code, 200)
        r = response.json()
        for item in r:
            assert self.user_fields.issubset(set(item.keys()))
            assert user.name in item['name']

    def test_create_user(self):
        c = APIClient()
        c.login_superuser()
        name = helper.fake_name()
        phone = helper.fake_phone()
        username = helper.fake_username()
        role = random.choice(const.UserRole.values)
        data = {
            'phone': phone,
            'name': name,
            'username': username,
            'password': '1234567890',
            'role': role,
        }
        response = c.post('/api/v1/users', data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        r = response.json()
        assert self.user_fields.issubset(set(r.keys()))
        assert User.objects.filter(username=username).exists()

        user = User.objects.get(username=username)
        assert user.check_password('1234567890')
        assert user.name == name
        assert user.phone == phone

    def test_retrieve_user(self):
        c = APIClient()
        c.login_superuser()
        response = c.get('/api/v1/users/{}'.format(self.user.id))
        r = response.json()
        self.assertEqual(response.status_code, 200)
        assert self.user_fields.issubset(set(r.keys()))

    def test_update_user(self):
        c = APIClient()
        c.login_superuser()
        user = self.user
        data = {
            'name': 'test',
            'password': '1234567890',
            'role': const.UserRole.SUPERUSER.value,
        }
        response = c.put(
            '/api/v1/users/{}'.format(user.id), data)
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.name == 'test'
        assert user.check_password('1234567890')
        assert user.role == const.UserRole.SUPERUSER.value

    def test_destroy_user(self):
        c = APIClient()
        c.login_superuser()
        user = self.user
        response = c.delete('/api/v1/users/{}'.format(user.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(id=user.id).exists())
