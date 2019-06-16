from django.contrib import admin


class ContractorAdmin(admin.ModelAdmin):
    """Contractor Admin"""
    list_per_page = 20
    readonly_fields = ('created', 'modified', 'deleted',)
    
    list_display = ('id', 'name', 'inn', 'kpp', 'address')
    list_filter =  ('name', 'inn', 'kpp', 'address')
    search_fields =  ('name', 'inn', 'kpp', 'address')