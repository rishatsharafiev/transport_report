from django.contrib import admin
from django.db.models import Sum, Count, Avg
from .models import *
from django.utils.safestring import mark_safe
from admin_totals.admin import ModelAdminTotals
import json

def getColumns(cls):
    res = [field.name for field in cls._meta.get_fields()][3:]
    res.insert(0, 'name_')
    res.insert(1, 'year_')
    return res


class ContractorsTotalAdmin(admin.ModelAdmin):
    def name_(self, obj):
        if obj.name == u'ВСЕГО':
            return mark_safe('<strong>%s</strong>' % obj.name)
        else:
            return obj.name
    name_.admin_order_field = 'name'
    name_.short_description = u'Подрядчик'

    def year_(self, obj):
        if obj.year.startswith(u'Итого'):
            return mark_safe('<strong>%s</strong>' % obj.year)
        else:
            return obj.year
    name_.admin_order_field = 'year'
    name_.short_description = u'Год'


    list_display = getColumns(ContractorsTotal)
    readonly_fields = [field.name for field in ContractorsTotal._meta.get_fields()]
    list_filter = ['name', 'year']
    ordering = ['id']


class ZonesTotalAdmin(admin.ModelAdmin):
    def name_(self, obj):
        if obj.name == u'ВСЕГО':
            return mark_safe('<strong>%s</strong>' % obj.name)
        else:
            return obj.name

    name_.admin_order_field = 'name'
    name_.short_description = u'Геозона'

    def year_(self, obj):
        if obj.year.startswith(u'Итого'):
            return mark_safe('<strong>%s</strong>' % obj.year)
        else:
            return obj.year

    name_.admin_order_field = 'year'
    name_.short_description = u'Год'

    list_display = getColumns(ZonesTotal)
    readonly_fields = [field.name for field in ZonesTotal._meta.get_fields()]
    list_filter = ['name', 'year']
    ordering = ['id']


class ObjectProgressAdmin(ModelAdminTotals):
    list_display = [field.name for field in ObjectProgress._meta.get_fields()][1:]
    readonly_fields = list_display
    list_filter = ['year', 'month', 'zone', 'contractor']
    ordering = ['id']
    list_totals = [('year', Count), ('price', Sum), ('finished_price', Sum), ('progress', Avg), ('finished_count', Count)]
    # list_totals = [('year', Sum), ('month', Sum), ('zone', Sum), ('contractor', Sum)]

class ObjectIntersectAdmin(ModelAdminTotals):
    list_display = [field.name for field in ObjectIntersect._meta.get_fields()][1:]
    readonly_fields = list_display
    ordering = ['id']
    list_totals = [('first_price', Sum), ('second_price', Sum)]
    
    def map(self, obj):
        pairs = [{
            "from_longitude":obj.first_longitude,
            "from_latitude":obj.first_latitude,
            "to_longitude":obj.second_longitude,
            "to_latitude":obj.second_latitude,
        }]
        result = '''<div 
            id="map" data-pairs={pairs} style="width: 100%; height: 400px; background: grey"
            />
        '''.format(pairs=json.dumps(pairs, default=float).replace(' ', ''))
        return mark_safe(result)

    map.short_description = 'Карта'
    readonly_fields = ('map',)
    class Media:
        css = {
            'all': ('https://js.api.here.com/v3/3.0/mapsjs-ui.css?dp-version=1549984893',),
        }
        js = (
            'https://js.api.here.com/v3/3.0/mapsjs-core.js',
            'https://js.api.here.com/v3/3.0/mapsjs-service.js',
            'https://js.api.here.com/v3/3.0/mapsjs-ui.js',
            'https://js.api.here.com/v3/3.0/mapsjs-mapevents.js',
            'manage/main.js',
        )

admin.site.register(ContractorsTotal, ContractorsTotalAdmin)
admin.site.register(ZonesTotal, ZonesTotalAdmin)
admin.site.register(ObjectProgress, ObjectProgressAdmin)
admin.site.register(ObjectIntersect, ObjectIntersectAdmin)
