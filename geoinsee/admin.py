from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from geoinsee.models import State
from geoinsee.models import Division
from geoinsee.models import County
from geoinsee.models import EmploymentZone
from geoinsee.models import Locality
from geoinsee.models import District


class DivisionFilter(admin.SimpleListFilter):
    title = _('division')
    parameter_name = 'divison_code_exact'

    def lookups(self, request, model_admin):
        for arg in request.GET:
            if arg.startswith('state'):
                state = State.objects.get(code=request.GET.get(arg))
                divisions = Division.objects.filter(state=state)
                return tuple([(i.code, i.name)for i in divisions])
        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(division=self.value())
        return queryset


class StateAdmin(admin.ModelAdmin):
    raw_id_fields = ('admin',)
    search_fields = ['name']
admin.site.register(State, StateAdmin)


class DivisionAdmin(admin.ModelAdmin):
    list_filter = ('state',)
    list_display = ('name', 'state',)
    raw_id_fields = ('admin',)
    search_fields = ['name']
admin.site.register(Division, DivisionAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_filter = ('state', 'division')
    list_display = ('name', 'state', 'division',)
    raw_id_fields = ('admin',)
    search_fields = ['name']
admin.site.register(District, DistrictAdmin)


class CountyAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(County, CountyAdmin)


class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'zipcode', 'state', 'division',)
    search_fields = ['name', 'zipcode', 'code']
    raw_id_fields = ('county', 'employmentzone',)
    list_filter = ('state', DivisionFilter,)
admin.site.register(Locality, LocalityAdmin)


class EmploymentZoneAdmin(admin.ModelAdmin):
    pass
admin.site.register(EmploymentZone, EmploymentZoneAdmin)
