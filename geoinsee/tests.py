"""Geoinsee test views"""
from django.test import TestCase
from django.test import Client

from geoinsee.models import Locality
from geoinsee.models import State
from geoinsee.models import Division


class BaseViewTestCase(TestCase):
    urls = 'geoinsee.urls'
    fixtures = ['geoinsee_test.json']
    model = State

    def get_response(self):
        item = self.model.objects.all()[0]
        url = item.get_absolute_url()
        response = self.client.get(url, follow=True)
        return response

    def test_template_used(self):
        response = self.get_response()
        template_name = 'geoinsee/%s_detail.html' % self.model.__name__.lower()
        self.assertTemplateUsed(response, template_name)

    def test_context(self):
        response = self.get_response()
        self.assertTrue(isinstance(response.context['object'], self.model))

    def test_status_code(self):
        response = self.get_response()
        self.assertEquals(response.status_code, 200)


class StateListViewTest(BaseViewTestCase):
    model = State

    def test_notfound(self):
        c = Client()
        response = c.get('/xxxx/')
        self.assertEquals(response.status_code, 404)


class DivisionListViewTest(BaseViewTestCase):
    model = Division

    def test_notfound(self):
        c = Client()
        response = c.get('/champagne-ardenne/xxxx_75/')
        self.assertEquals(response.status_code, 404)


class LocalityListViewTest(BaseViewTestCase):
    model = Locality

    def test_notfound(self):
        c = Client()
        response = c.get('/champagne-ardenne/marne_51/xxxxx_51241/')
        self.assertEquals(response.status_code, 404)
