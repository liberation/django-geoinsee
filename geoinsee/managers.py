"""Model managers for geoinsee"""
from django.db import models


class LocalityManager(models.Manager):
    def get_queryset(self):
        qs = super(LocalityManager, self).get_queryset()
        return qs.select_related('division')
