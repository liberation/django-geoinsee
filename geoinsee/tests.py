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
    urls = 'geoinsee.urls'
    fixtures = ['test.json']
    model = State

    def test_status_code(self):
        item = self.model.objects.all()[0]
        url = item.get_absolute_url()
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)


class StateListViewTest(BaseViewTestCase):
    model = State


class DivisionListViewTest(BaseViewTestCase):
    model = Division


class LocalityListViewTest(BaseViewTestCase):
    model = Locality
