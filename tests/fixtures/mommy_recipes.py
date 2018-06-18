# -*- coding: utf-8 -*-
from model_mommy.recipe import Recipe

from apps.backend.models import User
from . import helper


user = Recipe(
    User,
    username=helper.fake_username,
    password=helper.fake_password,
    name=helper.fake_name,
    phone=helper.fake_phone,
    role=helper.fake_role,
)
