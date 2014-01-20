"""Geoinsee test views"""
from decimal import Decimal
from django.test import TestCase
from django.test.client import Client

from geoinsee.models import Locality
from geoinsee.models import State
from geoinsee.models import Division
from geoinsee.models import District
from geoinsee.models import County
from geoinsee.models import EmploymentZone


class BaseViewTestCase(TestCase):
    fixtures = ['test.json']


class StateListViewTest(BaseViewTestCase):

    def test_bla(self):
        print Locality.objects.count()
