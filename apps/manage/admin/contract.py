import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from .inlines import ContractObjectInline


class ContractAdmin(admin.ModelAdmin):
    """Contract Admin"""
    list_per_page = 20

    def map(self, obj):
        contract_objects = obj.contractobject_set.all()
        pairs = [{
            "from_longitude":co.from_longitude,
            "from_latitude":co.from_latitude,
            "to_longitude":co.to_longitude,
            "to_latitude":co.to_latitude,
        } for co in contract_objects if co.from_latitude and co.to_longitude and co.to_latitude]
        print(contract_objects)
        result = '''<div 
            id="map" data-pairs={pairs} style="width: 100%; height: 400px; background: grey"
            />
        '''.format(pairs=json.dumps(pairs, default=float).replace(' ', ''))
        return mark_safe(result)

    readonly_fields = ('created', 'modified', 'deleted', 'map',)

    inlines = (ContractObjectInline,)

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
