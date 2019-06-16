import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from .inlines import ObjectProgressInline


class ContractObjectAdmin(admin.ModelAdmin):
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

    readonly_fields = ('created', 'modified', 'deleted', 'map',)

    inlines = (ObjectProgressInline,)

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
