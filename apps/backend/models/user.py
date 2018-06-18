# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from apps.backend import const
from .base import BaseModel


__all__ = ['User']


class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('role', const.UserRole.USER.value)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        if not password:
            raise ValueError('Superuser must have password')

        extra_fields['role'] = const.UserRole.SUPERUSER.value
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=32, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=10, choices=const.UserRole.choices)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['phone']),
        ]
        ordering = ['-id']

    def __str__(self):
        return 'User(id: {}, name: {})'.format(self.id, self.get_full_name())

    def get_full_name(self):
        return self.name or self.phone or self.username

    def get_short_name(self):
        return self.get_full_name()

    @property
    def is_admin(self):
        return self.role in const.UserRole.admin_roles

    @property
    def is_staff(self):
        return self.role in const.UserRole.staff_roles

    @property
    def is_superuser(self):
        return self.role == const.UserRole.SUPERUSER.value
