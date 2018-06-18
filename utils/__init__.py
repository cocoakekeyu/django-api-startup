# -*- coding: utf-8 -*-
import random


def is_phonenumber(value):
    if len(str(value)) != 11:
        return False
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False
    return True


def sub_dict(d, keys):
    return dict([(k, d[k]) for k in keys if k in d])


def sample_wr(iterable, choose=random.choice):
    while True:
        yield choose(iterable)


class cached_property(object):

    def __init__(self, wrapped, name=None):
        self.wrapped = wrapped
        self.__doc__ = getattr(wrapped, '__doc__', None)
        self.name = name or wrapped.__name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        name = self.name
        result = self.wrapped(inst)
        setattr(inst, name, result)
        return result
