# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models


__all__ = ['SoftDeletionMixin', 'BaseModel']


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return super(SoftDeletionManager, self).get_queryset().\
                filter(deleted_at=None)
        return super(SoftDeletionManager, self).get_queryset()


class SoftDeletionMixin(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.is_delete = True
        self.save()

    def hard_delete(self):
        super(SoftDeletionMixin, self).delete()


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
