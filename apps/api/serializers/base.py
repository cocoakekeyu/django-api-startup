# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


__all__ = ['BaseSerializer', 'BaseModelSerializer', 'IDPermitSerializer',
           'IDPermitListSerializer']


class CommonMixin(object):

    @property
    def current_user(self):
        return getattr(self, 'context', {}).get('current_user')

    @property
    def current_app(self):
        return getattr(self, 'context', {}).get('current_app')

    @property
    def is_staff(self):
        return getattr(self, 'context', {}).get('is_staff')

    @property
    def is_admin(self):
        return getattr(self, 'context', {}).get('is_admin')

    @property
    def is_superuser(self):
        return getattr(self, 'context', {}).get('is_superuser')


class BaseModelSerializer(CommonMixin, serializers.ModelSerializer):
    pass


class BaseSerializer(CommonMixin, serializers.Serializer):
    pass


class IDPermitSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        self.model_class = kwargs.pop('model_class', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if self.model_class:
            try:
                result = self.model_class.objects.get(id=data['id'])
            except ObjectDoesNotExist:
                detail = {'id': 'resource id not found'}
                raise serializers.ValidationError(detail)
            return result
        return data


class IDPermitListSerializer(serializers.ListSerializer):

    def __init__(self, keep_order=False, *args, **kwargs):
        self.keep_order = keep_order
        self.model_class = kwargs.pop('model_class', None)
        kwargs['child'] = kwargs.get('child', IDPermitSerializer())
        super().__init__(*args, **kwargs)

    def validate(self, data):
        try:
            ids = [item['id'] for item in data]
        except KeyError:
            detail = {'id': 'this field required'}
            raise serializers.ValidationError(detail)
        if self.model_class:
            result = self.model_class.objects.filter(id__in=ids)
            if len(result) != len(ids):
                detail = {'id': 'resource id not found'}
                raise serializers.ValidationError(detail)
            if self.keep_order:
                result = sorted(result, key=lambda x: ids.index(x.id))
            return result
        return ids
