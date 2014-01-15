# -*- coding: utf-8 -*-
"""geo insee models"""
from decimal import Decimal
from math import degrees
from math import radians
from math import cos

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

from geoinsee.constants import COUNTY_TYPE
from geoinsee.constants import LOCALITY_TYPE
from geoinsee.managers import LocalityManager
from geoinsee.utils import distance
from geoinsee.utils import EARTH_RADIUS_KM


class State(models.Model):
    code = models.CharField(
        max_length=3,
        primary_key=True)

    name = models.CharField(
        max_length=200,
        db_index=True)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    admin = models.ForeignKey(
        'Locality',
        related_name='state_admin',
        null=True)

    class Meta:
        verbose_name = u"région"
        verbose_name_plural = u"régions"

    def get_absolute_url(self):
        return reverse('geoinsee_state', kwargs={
            'slug': self.slug
        })

    def get_breadcrumbs(self):
        return [self]

    def __unicode__(self):
        return self.name


class Division(models.Model):
    code = models.CharField(
        max_length=3,
        primary_key=True)

    name = models.CharField(
        max_length=200,
        db_index=True)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    state = models.ForeignKey(
        'State',
        related_name='division_state')

    admin = models.ForeignKey(
        'Locality',
        related_name='division_admin')

    class Meta:
        verbose_name = u"département"
        verbose_name_plural = u"départements"

    def get_absolute_url(self):
        return reverse('geoinsee_division', kwargs={
            'slug': self.slug,
            'code': self.code
        })

    @cached_property
    def get_breadcrumbs(self):
        return [self.state, self]

    def __unicode__(self):
        return self.name


class District(models.Model):
    code = models.CharField(
        max_length=8,
        primary_key=True)

    name = models.CharField(
        max_length=200,
        db_index=True)

    prefix = models.CharField(
        max_length=5)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    state = models.ForeignKey(
        'State',
        related_name='district_state')

    division = models.ForeignKey(
        'Division',
        related_name='district_division')

    admin = models.ForeignKey(
        'Locality',
        related_name='district_admin')

    class Meta:
        verbose_name = u"Arrondissement"
        verbose_name_plural = u"Arrondissements"


    @cached_property
    def get_breadcrumbs(self):
        return [self.state, self.division, self]

    def __unicode__(self):
        if self.prefix:
            return u"%s%s" % (self.prefix, self.name)
        return self.name


# class SubDivision(models.Model):
#     code = models.CharField(
#         max_length=3,
#         primary_key=True)

#     name = models.CharField(
#         max_length=200,
#         db_index=True)

#     prefix = models.CharField(
#         max_length=5)

#     slug = models.CharField(
#         max_length=200,
#         db_index=True)

#     state = models.ForeignKey(
#         'State',
#         related_name='subdivision_state')

#     division = models.ForeignKey(
#         'Division',
#         related_name='subdivision_division')

#     admin = models.ForeignKey(
#         'Locality',
#         related_name='subdivision_admin')

#     def __unicode__(self):
#         if self.prefix:
#             return u"%s%s" % (self.prefix, self.name)
#         return self.name


class County(models.Model):
    code = models.PositiveIntegerField(
        primary_key=True)

    name = models.CharField(
        max_length=200)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    typology = models.CharField(
        max_length=2,
        db_index=True,
        choices=COUNTY_TYPE)

    class Meta:
        verbose_name = u"intercommunalité"
        verbose_name_plural = u"intercommunalités"

    @cached_property
    def get_breadcrumbs(self):
        return [self.state, self.division, self]

    def __unicode__(self):
        return self.name


class Locality(models.Model):
    code = models.CharField(
        max_length=10,
        primary_key=True)

    name = models.CharField(
        max_length=200,
        db_index=True)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    zipcode = models.CharField(
        max_length=5,
        db_index=True,
        null=True)

    typology = models.CharField(
        max_length=3,
        db_index=True,
        choices=LOCALITY_TYPE)

    surface = models.PositiveIntegerField(
        null=True)
    population = models.PositiveIntegerField(
        db_index=True)

    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True)

    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=9,
        null=True)

    state = models.ForeignKey(
        'State',
        null=True)

    division = models.ForeignKey(
        'Division',
        null=True)

    district = models.ForeignKey(
        'District',
        null=True)

    county = models.ForeignKey(
        'County',
        null=True)

    employmentzone = models.ForeignKey(
        'EmploymentZone',
        null=True)

    objects = LocalityManager()

    class Meta:
        verbose_name = u"commune"
        verbose_name_plural = u"communes"

    @cached_property
    def get_breadcrumbs(self):
        return [self.state, self.division, self]

    @property
    def get_employmentzone(self):
        return self.employmentzone

    @classmethod
    def _near_localities(self, lat, lon, km):
        diff_lat = Decimal(str(degrees(km / EARTH_RADIUS_KM)))
        latitude = Decimal(lat)
        longitude = Decimal(lon)
        max_lat = latitude + diff_lat
        min_lat = latitude - diff_lat
        diff_long = Decimal(str(
                        degrees(km / EARTH_RADIUS_KM / cos(radians(latitude)))
                    ))
        max_long = longitude + diff_long
        min_long = longitude - diff_long
        near_localities = Locality.objects.filter(
                                latitude__gte=min_lat,
                                longitude__gte=min_long)
        near_localities = near_localities.filter(
                                latitude__lte=max_lat,
                                longitude__lte=max_long)

        for i in near_localities:
            current = [latitude, longitude]
            target = [i.latitude, i.longitude]
            i.geo_dist = distance(current, target)
        return list(near_localities)

    @classmethod
    def near_location_rough(self, lat, lon):
        return self._near_localities(lat, lon, 3)

    def near_localities_rough(self, km):
        """
        Rough calculation of the localities at 'miles' miles of this locality.
        Is rough because calculates a square instead of a circle and the earth
        is considered as an sphere, but this calculation is fast! And we don't
        need precission.
        """
        if not self.longitude or not self.latitude:
            return []
        localities = self._near_localities(self.latitude, self.longitude, km)
        if self in localities:
            localities.remove(self)
        return localities

    def get_absolute_url(self):
        return reverse('geoinsee_locality', kwargs={
            'locality_slug': self.slug,
            'zipcode': self.zipcode,
            'division_slug': self.division.slug,
            'division_code': self.division.code
        })

    def __unicode__(self):
        return self.name


class EmploymentZone(models.Model):
    code = models.PositiveIntegerField(
        primary_key=True)

    name = models.CharField(
        max_length=200)

    slug = models.CharField(
        max_length=200,
        db_index=True)

    class Meta:
        verbose_name = u"zone emploi"
        verbose_name_plural = u"zones emploi"

    def __unicode__(self):
        return self.name
