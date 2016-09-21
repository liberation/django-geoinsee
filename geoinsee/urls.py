"""geo insee urls"""
from django.conf.urls import url
from django.conf.urls import patterns

from geoinsee.views import DivisionView
from geoinsee.views import LocalityView
from geoinsee.views import LocalitySearchView
from geoinsee.views import StateView
from geoinsee.views import StateListView


urlpatterns = patterns(
    '',
    # search
    url(r'^search/$',
        LocalitySearchView.as_view(),
        name='geoinsee_locality_search'),
    # locality
    url(r'^(?P<division_slug>[-\w]+)_(?P<division_code>[AB\d]+)/'
        '(?P<locality_slug>[-\w]+)_(?P<zipcode>\d+)/$',
        LocalityView.as_view(),
        name='geoinsee_locality'),
    # division
    url(r'^(?P<slug>[-\w]+)_(?P<code>[AB\d]+)/$',
        DivisionView.as_view(),
        name='geoinsee_division'),
    # state
    url(r'^(?P<slug>[-\w]+)/$',
        StateView.as_view(),
        name='geoinsee_state'),
    # index
    url(r'^$',
        StateListView.as_view(),
        name='geoinsee_index'),
)
