# -*- coding: utf-8 -*-
import enum


# https://github.com/mkaplenko/python-classproperty/blob/master/class_property/
# descriptor.py
class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("Can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


def normalize_to_choices(value):
    if isinstance(value, (tuple, list)):
        if len(value) == 1:
            value = value[0]
        elif len(value) > 1:
            return tuple(value[:2])
    return (value, value)


@enum.unique
class Base(enum.Enum):

    @property
    def value(self):
        ret = super().value
        if isinstance(ret, (tuple, list)):
            try:
                ret = ret[0]
            except IndexError:
                pass
        return ret

    @property
    def raw_value(self):
        return super().value

    @classproperty
    def names(self):
        return [i.name for i in self]

    @classproperty
    def values(self):
        return [i.value for i in self]

    @classproperty
    def choices(self):
        return sorted([normalize_to_choices(i.raw_value) for i in self])


class UserRole(Base):
    USER = ('user', '用户')
    ADMIN = ('admin', '管理员')
    SUPERUSER = ('superuser', '超级管理员')

    @classproperty
    def admin_roles(self):
        roles = [self.ADMIN, self.SUPERUSER]
        return [i.value for i in roles]

    @classproperty
    def staff_roles(self):
        roles = [self.ADMIN, self.SUPERUSER]
        return [i.value for i in roles]


class ClientAppType(Base):
    APP = 'X-App'
    IOS = 'X-IOS'
    ANDROID = 'X-Android'
    WEB = 'X-Web'
    ADMIN = 'X-Admin'
