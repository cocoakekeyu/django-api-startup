# -*- coding: utf-8 -*-
import random

import faker

from apps.backend import const


fake = faker.Factory.create('zh_CN')


def fake_boolean():
    return random.choice([True, False])


def fake_role():
    return random.choice(const.UserRole.values)


def fake_name():
    return fake.name()


def fake_username():
    return fake_name()


def fake_password():
    return fake_name()


def fake_phone():
    return fake.phone_number()
