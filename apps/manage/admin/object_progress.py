from django.contrib import admin
from django.db.models import Sum, Count, Avg
from admin_totals.admin import ModelAdminTotals

class ObjectProgressAdmin(ModelAdminTotals):
    """ObjectProgress Admin"""
    list_per_page = 20
    readonly_fields = ('created', 'modified', 'deleted',)

    list_display = ('id', 'contract', 'contractobject', 'contractor', 'price', 'start_date', 'finish_date')
    list_filter = ('contract', 'contractor', 'start_date', 'finish_date')
    search_fields = ('contract__name', 'contractor__name',)
    list_totals = [('price', Sum),]