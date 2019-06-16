import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, Avg
from admin_totals.admin import ModelAdminTotals

from .inlines import ObjectProgressInline
from ..models import ContractObject

class ContractObjectAdmin(ModelAdminTotals):
    """Contractbject  Admin"""
    list_per_page = 20

    def map(self, obj):
        pairs = [{
            "from_longitude":obj.from_longitude,
            "from_latitude":obj.from_latitude,
            "to_longitude":obj.to_longitude,
            "to_latitude":obj.to_latitude,
        }]
        result = '''<div 
            id="map" data-pairs={pairs} style="width: 100%; height: 400px; background: grey"
            />
        '''.format(pairs=json.dumps(pairs, default=float).replace(' ', ''))
        return mark_safe(result)
    map.short_description = 'Карта'
    readonly_fields = ('created', 'modified', 'deleted', 'map',)

    inlines = (ObjectProgressInline,)
    list_display = ('id', 'contract', 'contractor', 'zone', 'price', 'start_date', 'finish_date')
    list_filter = ('contract', 'contractor', 'zone', 'start_date', 'finish_date')
    search_fields = ('contract__name', 'contractor__name',)
    list_totals = [('price', Sum),]
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
