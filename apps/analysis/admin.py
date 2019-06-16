from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


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


class ObjectProgressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ObjectProgress._meta.get_fields()][1:]
    readonly_fields = list_display
    list_filter = ['year', 'month', 'zone', 'contractor']
    ordering = ['id']


admin.site.register(ContractorsTotal, ContractorsTotalAdmin)
admin.site.register(ZonesTotal, ZonesTotalAdmin)
admin.site.register(ObjectProgress, ObjectProgressAdmin)

