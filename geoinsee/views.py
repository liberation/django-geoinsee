"""geo insee views"""
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from geoinsee.models import Locality
from geoinsee.models import State
from geoinsee.models import Division


class StateListView(ListView):
    """List all state by name"""
    model = State

    def get_queryset(self):
        qs = super(StateListView, self).get_queryset()
        return qs.order_by('slug')


class BaseDetailView(DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super(
                    BaseDetailView, self
                ).get_context_data(*args, **kwargs)
        context.update(self.get_extra_context())
        return context


class StateView(BaseDetailView):
    """Display a state detail and its division"""
    model = State

    def get_extra_context(self):
        divisions = self.object.division_state.all().order_by('slug')
        return {'divisions': divisions}

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs['slug'])


class DivisionView(BaseDetailView):
    """Display a division detail and its localities"""
    model = Division

    def get_extra_context(self):
        localities = self.object.locality_set.order_by('slug')\
                                .prefetch_related('division')
        return {'localities': localities}

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs['slug'],
                                      code=self.kwargs['code'])


class LocalityView(BaseDetailView):
    """Display a locality and near by localities"""
    model = Locality

    def get_extra_context(self):
        localities = self.object.near_localities_rough(5)
        return {'near_by_localities': localities}

    def get_object(self):
        return self.model.objects.prefetch_related(
                    'state', 'division',
                    'county', 'employmentzone'
                ).get(
                    slug=self.kwargs['locality_slug'],
                    zipcode=self.kwargs['zipcode'],
                    division__slug=self.kwargs['division_slug'],
                    division__code=self.kwargs['division_code'])


class LocalitySearchView(View):
    """Search view"""
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LocalitySearchView, self).dispatch(*args, **kwargs)

    def get_data(self):
        query = self.request.GET.get('query', '').lower().strip()
        content = {
            "query": query,
            "suggestions": []
        }
        # no query
        if not query:
            return content
        # is a zipcode
        elif query[0].isdigit():
            kwarg = 'zipcode__istartswith'
        # full name
        else:
            kwarg = 'name__istartswith'
        # query
        localities = Locality.objects.filter(**{kwarg: query})[:20]
        values = []
        for locality in localities:
            values.append({
                "value": locality.name,
                "url": locality.get_absolute_url(),
                "name": locality.name,
                "zipcode": locality.zipcode,
                "tokens": locality.name.split(' '),
                "division": locality.division.name,
                "state": locality.state.name,
            })
        return values

    def text(self):
        content = self.get_data()
        return json.dumps(content, indent=2)

    def post(self, request, *args, **kwargs):
        data = self.request.POST
        print data['lat'], data['lng']
        localities = Locality.near_location_rough(lat=data['lat'], lon=data['lng'])[:1]
        print localities
        if localities:
            return HttpResponse(
                json.dumps([localities[0].get_absolute_url()]),
                content_type='application/javascript'
            )

        return HttpResponse(
            json.dumps(['data']),
            content_type='application/javascript'
        )

    def get(self, request, *args, **kwargs):
        #print request
        return HttpResponse(
            self.text(),
            content_type='application/json'
        )
